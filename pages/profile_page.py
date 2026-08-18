import allure
from playwright.sync_api import Page

from pages.base_page import BasePage


class ProfilePage(BasePage):
    """Страница профиля пользователя."""

    def __init__(self, page: Page):
        super().__init__(page)

    @allure.step('Открыть профиль')
    def open(self):
        self.navigate('/profile')

    @allure.step('Обновить имя: {first_name}')
    def update_first_name(self, first_name: str):
        self.page.locator('input[name="first_name"]').fill(first_name)

    @allure.step('Обновить фамилию: {last_name}')
    def update_last_name(self, last_name: str):
        self.page.locator('input[name="last_name"]').fill(last_name)

    @allure.step('Обновить телефон: {phone}')
    def update_phone(self, phone: str):
        self.page.locator('input[name="phone"]').fill(phone)

    @allure.step('Загрузить аватар: {path}')
    def upload_avatar(self, path: str):
        self.page.locator('input[type="file"]').set_input_files(path)

    @allure.step('Сохранить профиль')
    def save(self):
        self.page.get_by_role('button', name='Сохранить').click()

    @allure.step('Получить значение поля: {field_name}')
    def get_field_value(self, field_name: str) -> str:
        locator = self.page.locator(f'input[name="{field_name}"]')
        locator.wait_for(state='visible')
        self.page.wait_for_function(
            f'document.querySelector(\'input[name="{field_name}"]\').value !== ""',
            timeout=5000,
        )
        return locator.input_value()

    @allure.step('Дождаться значения поля {field_name} = {expected}')
    def wait_field_value(self, field_name: str, expected: str, timeout: float = 5000):
        """Web-first ожидание: значение поля равно {expected}."""
        locator = self.page.locator(f'input[name="{field_name}"]')
        locator.wait_for(state='visible')
        self.page.wait_for_function(
            f'document.querySelector(\'input[name="{field_name}"]\').value === {expected!r}',
            timeout=timeout,
        )