import allure
from playwright.sync_api import Page

from pages.base_page import BasePage


class RegistrationPage(BasePage):
    """Страница регистрации."""

    def __init__(self, page: Page):
        super().__init__(page)

    @allure.step('Открыть страницу регистрации')
    def open(self):
        self.navigate('/register')

    @allure.step('Зарегистрироваться: {email}')
    def register(
        self,
        first_name: str,
        last_name: str,
        email: str,
        phone: str,
        password: str,
    ):
        self.page.locator('input[name="first_name"]').fill(first_name)
        self.page.locator('input[name="last_name"]').fill(last_name)
        self.page.locator('input[name="email"]').fill(email)
        self.page.locator('input[name="phone"]').fill(phone)
        self.page.locator('input[name="password"]').fill(password)
        self.page.get_by_role('button', name='Зарегистрироваться').click()