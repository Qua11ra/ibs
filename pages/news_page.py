import allure
from playwright.sync_api import Page, expect

from pages.base_page import BasePage


class NewsPage(BasePage):
    """Страница новостей: список, создание, детальная страница."""

    def __init__(self, page: Page):
        super().__init__(page)

    @allure.step('Открыть список новостей')
    def open_list(self):
        self.navigate('/')

    @allure.step('Получить заголовок первой новости')
    def get_first_news_title(self) -> str:
        return self.page.locator('h2 a').first.inner_text()

    @allure.step('Открыть новость: {title}')
    def open_news(self, title: str):
        self.page.get_by_role('link', name=title).click()

    @allure.step('Открыть новость по id: {news_id}')
    def open_news_by_id(self, news_id: int | str):
        self.navigate(f'/news/{news_id}')

    @allure.step('Открыть форму создания новости')
    def open_create_form(self):
        self.navigate('/news/create')

    @allure.step('Создать новость: {title}')
    def create_news(self, title: str, text: str, subtitle: str = '', tags: str = ''):
        self.page.locator('input[name="title"]').fill(title)
        self.page.locator('input[name="subtitle"]').fill(subtitle)
        self.page.locator('textarea[name="text"]').fill(text)
        self.page.locator('input[name="tags"]').fill(tags)
        self.page.get_by_role('button', name='Создать').click()

    @allure.step('Проверить валидацию поля: {field_name}')
    def is_field_invalid(self, field_name: str) -> bool:
        return self.page.locator(
            f'input[name="{field_name}"], textarea[name="{field_name}"]'
        ).evaluate('el => !el.checkValidity()')

    @allure.step('Дождаться invalid-состояния поля: {field_name}')
    def wait_field_invalid(self, field_name: str, timeout: float = 5000) -> bool:
        """Web-first ожидание: поле становится :invalid (required-валидация)."""
        self.page.wait_for_function(
            f'(() => {{ const els = document.querySelectorAll('
            f'"input[name=\\"{field_name}\\"]:invalid, '
            f'textarea[name=\\"{field_name}\\"]:invalid"); '
            f'return els.length > 0; }})()',
            timeout=timeout,
        )
        return True

    @allure.step('Дождаться первой новости с маркером: {marker}')
    def wait_first_news_contains(self, marker: str, timeout: float = 5000) -> bool:
        """Web-first ожидание: первая карточка содержит {marker} (XSS-тест)."""
        self.page.locator('h2 a').first.wait_for(state='visible', timeout=timeout)
        expect(
            self.page.locator('h2 a').first,
            message=f'Первая новость не содержит маркер {marker}',
        ).to_contain_text(marker, timeout=timeout)
        return True

    @allure.step('Получить заголовок новости (h1)')
    def get_news_title(self) -> str:
        return self.page.get_by_role('heading', level=1).inner_text()

    @allure.step('Получить подзаголовок новости (h2)')
    def get_news_subtitle(self) -> str:
        return self.page.get_by_role('heading', level=2).inner_text()

    @allure.step('Получить автора новости')
    def get_author(self) -> str:
        return self.page.locator('div.flex.items-center.gap-2.mb-4 span').first.inner_text()

    @allure.step('Получить дату новости')
    def get_date(self) -> str:
        return self.page.locator('div.flex.items-center.gap-2.mb-4 span').nth(2).inner_text()

    @allure.step('Проверить отображение «Новость не найдена»')
    def is_not_found(self, timeout: float = 5000) -> bool:
        locator = self.page.get_by_text('Новость не найдена')
        locator.wait_for(state='visible', timeout=timeout)
        return locator.is_visible()

    @allure.step('Подсчитать теги script, содержащие {marker}')
    def count_scripts_with_text(self, marker: str) -> int:
        """Проверка базовой безопасности: исполняемый `<script>` с маркером
        не должен попадать в DOM (XSS-тест)."""
        return self.page.locator('script', has_text=marker).count()