import logging
import os

import allure
import pytest
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright

from helpers.api_client import APIClient
from helpers.data_generator import generate_user
from helpers.soft_assertions import SoftAssertions
from pages.base_page import BASE_URL
from pages.login_page import LoginPage

logger = logging.getLogger('ibs_tests')

ARTIFACTS_DIRS = {
    'traces': 'traces',
    'screenshots': 'screenshots',
}


def pytest_addoption(parser):
    parser.addoption('--headed', action='store_true', help='Запуск браузера с UI')
    parser.addoption(
        '--browser',
        default='chromium',
        choices=['chromium', 'firefox', 'webkit'],
        help='Движок браузера',
    )
    parser.addoption(
        '--tracing',
        default='retain-on-failure',
        choices=['on', 'off', 'retain-on-failure'],
        help='Режим записи Playwright Trace',
    )
    parser.addoption(
        '--screenshot',
        default='only-on-failure',
        choices=['on', 'off', 'only-on-failure'],
        help='Режим сохранения скриншотов',
    )


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f'rep_{rep.when}', rep)


@pytest.fixture(scope='session')
def browser(request) -> Browser:
    """Один браузер на всю сессию."""
    headless = not request.config.getoption('--headed')
    browser_type = request.config.getoption('--browser')
    logger.info('Сессия: запуск браузера %s (headless=%s)', browser_type, headless)
    with sync_playwright() as p:
        browser = getattr(p, browser_type).launch(headless=headless)
        yield browser
        browser.close()
        logger.info('Сессия: браузер закрыт')


@pytest.fixture(scope='function')
def context(request, browser) -> BrowserContext:
    """Новый контекст на каждый тест: полная изоляция + tracing."""
    context = browser.new_context(
        viewport={'width': 1280, 'height': 720},
    )
    tracing_mode = request.config.getoption('--tracing')
    if tracing_mode != 'off':
        context.tracing.start(screenshots=True, snapshots=True)
    logger.info('Тест "%s": новый контекст создан (tracing=%s)', request.node.name, tracing_mode)

    yield context

    failed = hasattr(request.node, 'rep_call') and request.node.rep_call.failed
    should_retain = tracing_mode == 'on' or (
        tracing_mode == 'retain-on-failure' and failed
    )
    if should_retain:
        os.makedirs(ARTIFACTS_DIRS['traces'], exist_ok=True)
        trace_path = f"{ARTIFACTS_DIRS['traces']}/{request.node.name}.zip"
        context.tracing.stop(path=trace_path)
        if failed:
            allure.attach.file(
                trace_path,
                name='Playwright Trace',
                attachment_type=allure.attachment_type.ZIP,
            )
        logger.info('Тест "%s": trace сохранён (%s)', request.node.name, trace_path)
    else:
        context.tracing.stop()

    context.close()


@pytest.fixture(scope='function')
def page(context: BrowserContext) -> Page:
    """Страница на каждый тест."""
    page = context.new_page()
    yield page
    page.close()


@pytest.fixture(scope='function', autouse=True)
def attach_screenshot_on_failure(page: Page, request):
    """Полноэкранный скриншот при падении теста + прикрепление в Allure."""
    yield
    failed = hasattr(request.node, 'rep_call') and request.node.rep_call.failed
    screenshot_mode = request.config.getoption('--screenshot')
    should_save = screenshot_mode == 'on' or (
        screenshot_mode == 'only-on-failure' and failed
    )
    if should_save:
        os.makedirs(ARTIFACTS_DIRS['screenshots'], exist_ok=True)
        screenshot_path = f"{ARTIFACTS_DIRS['screenshots']}/{request.node.name}.png"
        page.screenshot(path=screenshot_path, full_page=True)
        if failed:
            allure.attach.file(
                screenshot_path,
                name='Screenshot',
                attachment_type=allure.attachment_type.PNG,
            )
    if failed:
        logger.error('Тест "%s" ПРОВАЛЕН: артефакты сохранены', request.node.name)
    else:
        logger.info('Тест "%s" завершён успешно', request.node.name)


@pytest.fixture
def soft_assertions() -> SoftAssertions:
    """Фикстура-обёртка над кастомным сборщиком мягких проверок."""
    return SoftAssertions()


@pytest.fixture(scope='session')
def api_client() -> APIClient:
    """HTTP-клиент для API-предусловий."""
    return APIClient()


@pytest.fixture
def registered_user(api_client: APIClient) -> dict:
    """Регистрация пользователя через API (предусловие для авторизации).

    API доступен (FastAPI archiscope.ru), поэтому предусловия делаем
    через API, а не через UI — это быстрее и стабильнее.
    """
    user = generate_user()
    response = api_client.register(user)
    assert response.status_code in (200, 201), (
        f'Не удалось зарегистрировать пользователя: '
        f'{response.status_code} {response.text}'
    )
    return user


@pytest.fixture
def logged_in_page(page: Page, registered_user: dict) -> Page:
    """Страница, авторизованная под зарегистрированным через API пользователем."""
    login_page = LoginPage(page)
    login_page.open()
    login_page.login(registered_user['email'], registered_user['password'])
    page.wait_for_url(f'{BASE_URL}/')
    return page