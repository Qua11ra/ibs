import allure
from playwright.sync_api import Page

BASE_URL = 'https://archiscope.ru'


class BasePage:
    """Базовый класс для всех страниц."""

    def __init__(self, page: Page):
        self.page = page

    @allure.step('Открыть {url}')
    def navigate(self, url: str):
        self.page.goto(f'{BASE_URL}{url}')

    @allure.step('Получить заголовок страницы')
    def get_title(self) -> str:
        return self.page.title()

    @allure.step('Сделать скриншот: {name}')
    def take_screenshot(self, name: str = 'page'):
        allure.attach(
            self.page.screenshot(),
            name=name,
            attachment_type=allure.attachment_type.PNG,
        )

    @allure.step('Получить текущий URL')
    def get_current_url(self) -> str:
        return self.page.url

    @allure.step('Открыть страницу входа')
    def open_login(self):
        self.navigate('/login')

    @allure.step('Открыть страницу регистрации')
    def open_register(self):
        self.navigate('/register')

    @allure.step('Перейти к созданию новости')
    def open_create_news(self):
        self.page.get_by_role('link', name='+ Добавить новость').click()

    @allure.step('Открыть меню профиля')
    def open_profile_menu(self):
        self.page.locator('.navbar .dropdown [role="button"]').click()

    @allure.step('Перейти в профиль')
    def open_profile(self):
        self.open_profile_menu()
        self.page.get_by_role('link', name='Профиль').click()

    @allure.step('Выйти из аккаунта')
    def logout(self):
        self.open_profile_menu()
        self.page.get_by_role('button', name='Выйти').click()