import allure
from faker import Faker
from playwright.sync_api import expect

from pages.profile_page import ProfilePage

fake = Faker('ru_RU')


@allure.epic('Профиль')
@allure.feature('Обновление профиля')
class TestProfile:
    @allure.story('Смена имени с проверкой сохранения')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description(
        'Смена имени в профиле: сообщение «Профиль обновлён», новое имя '
        'в поле формы и сохранение после перезагрузки страницы.'
    )
    def test_update_profile_name(self, logged_in_page, soft_assertions):
        """Обновление имени в профиле и проверка, что данные сохранились."""
        profile_page = ProfilePage(logged_in_page)

        with allure.step('Открыть профиль и дождаться загрузки данных'):
            profile_page.open()
            old_name = profile_page.get_field_value('first_name')

        new_name = fake.first_name()
        soft_assertions.check(
            old_name != new_name,
            'Сгенерированное новое имя совпадает с текущим — тест некорректен',
        )

        with allure.step(f'Обновить имя на «{new_name}» и сохранить'):
            profile_page.update_first_name(new_name)
            profile_page.save()

        with allure.step('Проверить сообщение об успешном обновлении'):
            expect(logged_in_page.get_by_text('Профиль обновлён')).to_be_visible()

        with allure.step('Проверить, что поле формы содержит новое имя'):
            assert profile_page.get_field_value('first_name') == new_name

        with allure.step('Перезагрузить страницу и проверить, что имя сохранилось'):
            logged_in_page.reload()
            profile_page.wait_field_value('first_name', new_name)

        soft_assertions.assert_all()
