import allure
from playwright.sync_api import expect

from helpers.data_generator import generate_user
from pages.base_page import BASE_URL
from pages.login_page import LoginPage
from pages.registration_page import RegistrationPage


@allure.epic('Авторизация')
@allure.feature('Регистрация')
class TestAuth:
    @allure.story('Полный цикл: регистрация -> редирект -> логин')
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description(
        'Регистрация нового пользователя с Faker-данными через UI, '
        'проверка редиректа на /login и вход созданным пользователем.'
    )
    def test_full_auth_cycle(self, page):
        """Регистрация -> редирект на /login -> логин созданным пользователем.

        Критично: полный цикл жизненного пути пользователя — регистрация
        и последующий вход должны работать с одной и той же учёткой.
        """
        user = generate_user()

        registration_page = RegistrationPage(page)
        registration_page.open()

        with allure.step('Заполнить форму регистрации Faker-данными'):
            registration_page.register(
                first_name=user['first_name'],
                last_name=user['last_name'],
                email=user['email'],
                phone=user['phone'],
                password=user['password'],
            )

        with allure.step('Проверить редирект на страницу входа'):
            expect(page).to_have_url(f'{BASE_URL}/login')

        with allure.step('Войти созданным пользователем'):
            login_page = LoginPage(page)
            login_page.login(user['email'], user['password'])

        with allure.step('Проверить успешный вход: редирект на главную, доступно создание новости'):
            expect(page).to_have_url(f'{BASE_URL}/')
            expect(page.get_by_role('link', name='+ Добавить новость')).to_be_visible()
