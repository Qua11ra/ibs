import allure
from playwright.sync_api import Page

from pages.base_page import BasePage


class LoginPage(BasePage):
    """Страница авторизации."""

    def __init__(self, page: Page):
        super().__init__(page)

    @allure.step('Открыть страницу входа')
    def open(self):
        self.navigate('/login')

    @allure.step('Войти как {email}')
    def login(self, email: str, password: str):
        self.page.locator('input[type="email"]').fill(email)
        self.page.locator('input[type="password"]').fill(password)
        self.page.get_by_role('button', name='Войти').click()

    @allure.step('Получить сообщение об ошибке')
    def get_error_message(self) -> str:
        return self.page.locator('.alert-error').inner_text()