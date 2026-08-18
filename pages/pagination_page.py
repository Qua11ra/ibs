import allure
from playwright.sync_api import Page, TimeoutError, expect

from pages.base_page import BasePage


class PaginationPage(BasePage):
    """Страница списка новостей с пагинацией."""

    def __init__(self, page: Page):
        super().__init__(page)

    @allure.step('Открыть список новостей')
    def open(self):
        self.navigate('/')

    @allure.step('Перейти на страницу {page_number}')
    def go_to_page(self, page_number: int):
        self.page.get_by_role('button', name=str(page_number)).click()

    @allure.step('Перейти на предыдущую страницу')
    def go_to_previous(self):
        self.page.get_by_role('button', name='«').click()

    @allure.step('Перейти на следующую страницу')
    def go_to_next(self):
        self.page.get_by_role('button', name='»').click()

    @allure.step('Получить заголовок первой новости')
    def get_first_news_title(self) -> str:
        return self.page.locator('h2 a').first.inner_text()

    @allure.step('Получить номер активной страницы')
    def get_active_page(self) -> str:
        return self.page.locator('button.btn-primary').inner_text()

    @allure.step('Дождаться активной страницы: {page_number}')
    def wait_active_page(self, page_number: int, timeout: float = 5000):
        """Web-first ожидание: активная кнопка пагинации равна {page_number}."""
        expect(
            self.page.locator('button.btn-primary'),
            message=f'Активная страница не равна {page_number}',
        ).to_have_text(str(page_number), timeout=timeout)

    @allure.step('Дождаться заголовка первой новости: {title}')
    def wait_first_news_title(self, title: str, timeout: float = 5000):
        """Web-first ожидание: заголовок первой новости равен {title}."""
        expect(
            self.page.locator('h2 a').first,
            message=f'Первая новость не равна «{title}»',
        ).to_have_text(title, timeout=timeout)

    @allure.step('Проверить наличие кнопки страницы {page_number}')
    def has_page_button(self, page_number: int, timeout: float = 5000) -> bool:
        """Web-first ожидание: кнопка страницы отображается.

        Кнопки пагинации рендерятся SPA-приложением асинхронно после загрузки
        данных, поэтому `is_visible()` без ожидания даёт ложный False.
        """
        try:
            self.page.get_by_role('button', name=str(page_number)).wait_for(
                state='visible',
                timeout=timeout,
            )
            return True
        except TimeoutError:
            return False