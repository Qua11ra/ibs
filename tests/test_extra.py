import uuid

import allure
from playwright.sync_api import expect

from pages.base_page import BASE_URL, BasePage
from pages.news_page import NewsPage


@allure.epic('Безопасность')
@allure.feature('Выход из аккаунта')
class TestLogout:
    @allure.story('Логаут из приложения')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description(
        'Тест на логаут: критичен для безопасности — после выхода сессия '
        'должна завершаться, пользователь возвращается на /login, '
        'а гостевые элементы навбара снова доступны.'
    )
    def test_logout(self, logged_in_page):
        """Выход из аккаунта завершает сессию и редиректит на /login."""
        with allure.step('Выполнить логаут через меню профиля'):
            base_page = BasePage(logged_in_page)
            base_page.logout()

        with allure.step('Проверить редирект на страницу входа'):
            expect(logged_in_page).to_have_url(f'{BASE_URL}/login')

        with allure.step('Проверить, что гостевой навбар снова доступен'):
            expect(logged_in_page.get_by_role('link', name='Войти')).to_be_visible()
            expect(logged_in_page.get_by_role('link', name='Регистрация')).to_be_visible()


@allure.epic('Безопасность')
@allure.feature('XSS')
class TestXss:
    @allure.story('XSS в заголовке новости')
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description(
        'Тест на XSS в заголовке новости: проверка базовой безопасности. '
        'Заголовок с <script> должен отображаться как обычный текст, '
        'а не исполняться (нет alert, нет тега script в DOM).'
    )
    def test_xss_in_news_title(self, logged_in_page, soft_assertions):
        """XSS-заголовок новости не должен исполняться браузером."""
        marker = f'__xss_{uuid.uuid4().hex[:8]}'
        xss_title = f'<script>window.{marker}=1</script>'
        dialogs = []
        logged_in_page.on('dialog', lambda dialog: dialogs.append(dialog.message))

        news_page = NewsPage(logged_in_page)

        with allure.step('Создать новость с XSS-заголовком'):
            news_page.open_create_form()
            news_page.create_news(title=xss_title, text='XSS check')

        with allure.step('Проверить редирект на список новостей'):
            expect(logged_in_page).to_have_url(f'{BASE_URL}/')

        with allure.step('Проверить, что заголовок отображается как текст'):
            assert news_page.wait_first_news_contains(marker), (
                f'Первая новость не содержит XSS-маркер {marker}'
            )

        with allure.step('Проверить, что в DOM нет исполняемого тега script с маркером'):
            assert news_page.count_scripts_with_text(marker) == 0, (
                'Найдён исполняемый <script> с XSS-маркером — заголовок не экранируется'
            )

        with allure.step('Проверить, что alert/диалог не сработал'):
            soft_assertions.check(not dialogs, f'Сработал диалог: {dialogs}')
            soft_assertions.assert_all()
