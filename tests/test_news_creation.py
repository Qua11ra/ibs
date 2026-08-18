import allure
from playwright.sync_api import expect

from helpers.data_generator import generate_news
from pages.base_page import BASE_URL
from pages.news_page import NewsPage


@allure.epic('Новости')
@allure.feature('Создание новости')
class TestNewsCreationSadPath:
    @allure.story('Sad Path: новость без заголовка')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description(
        'Создание новости с пустым заголовком: браузерная required-валидация '
        'должна остановить отправку формы (POST не уходит, URL не меняется).'
    )
    def test_create_news_without_title(self, logged_in_page):
        """Создание новости без заголовка — ошибка валидации."""
        news = generate_news()
        news_page = NewsPage(logged_in_page)

        with allure.step('Открыть форму создания новости'):
            news_page.open_create_form()

        with allure.step('Отправить форму с пустым заголовком и заполненным текстом'):
            news_page.create_news(title='', text=news['text'])

        with allure.step('Проверить, что поле title невалидно (required)'):
            assert news_page.wait_field_invalid('title'), (
                'Поле title не стало невалидным после submit с пустым заголовком'
            )

        with allure.step('Проверить, что URL не изменился — форма не отправлена'):
            expect(logged_in_page).to_have_url(f'{BASE_URL}/news/create')

    @allure.story('Sad Path: новость без текста')
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description(
        'Создание новости с пустым текстом: браузерная required-валидация '
        'должна остановить отправку формы (POST не уходит, URL не меняется).'
    )
    def test_create_news_without_text(self, logged_in_page):
        """Создание новости без текста — ошибка валидации."""
        news = generate_news()
        news_page = NewsPage(logged_in_page)

        with allure.step('Открыть форму создания новости'):
            news_page.open_create_form()

        with allure.step('Отправить форму с заполненным заголовком и пустым текстом'):
            news_page.create_news(title=news['title'], text='')

        with allure.step('Проверить, что поле text невалидно (required)'):
            assert news_page.wait_field_invalid('text'), (
                'Поле text не стало невалидным после submit с пустым текстом'
            )

        with allure.step('Проверить, что URL не изменился — форма не отправлена'):
            expect(logged_in_page).to_have_url(f'{BASE_URL}/news/create')
