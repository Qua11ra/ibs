import re

import allure
from playwright.sync_api import expect

from pages.news_page import NewsPage


@allure.epic('Новости')
@allure.feature('Детальная страница новости')
class TestNewsDetail:
    @allure.story('Успешный просмотр новости')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description(
        'Переход из списка на детальную страницу: URL /news/{id}, '
        'заголовок h1 совпадает с названием новости, текст отображается.'
    )
    def test_view_existing_news(self, page):
        """Успешный просмотр новости из списка."""
        news_page = NewsPage(page)

        with allure.step('Открыть список новостей и получить заголовок первой'):
            news_page.open_list()
            first_title = news_page.get_first_news_title()

        with allure.step('Перейти на детальную страницу новости'):
            news_page.open_news(first_title)

        with allure.step('Проверить URL /news/{id} и заголовок h1'):
            expect(page).to_have_url(re.compile(r'/news/\d+'))
            expect(page.get_by_role('heading', level=1)).to_have_text(first_title)

        with allure.step('Проверить, что текст новости отображается'):
            expect(page.locator('p').first).to_be_visible()

    @allure.story('Переход на несуществующую новость / 404')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description(
        'Открытие /news/{несуществующий_id}: приложение должно '
        'показать «Новость не найдена», а не упасть в исключение.'
    )
    def test_nonexistent_news_shows_404(self, page):
        """Несуществующая новость отдаёт страницу 404."""
        news_page = NewsPage(page)

        with allure.step('Открыть несуществующую новость'):
            news_page.open_news_by_id(999999)

        with allure.step('Проверить отображение «Новость не найдена»'):
            assert news_page.is_not_found(), (
                'Для /news/999999 не отобразилась страница «Новость не найдена»'
            )

    @allure.story('Отображение автора и даты')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description(
        'На детальной странице должны отображаться автор и дата новости '
        '(метаданные из карточки). Проверки собраны через SoftAssertions.'
    )
    def test_news_shows_author_and_date(self, page, soft_assertions):
        """Автор и дата отображаются на детальной странице."""
        news_page = NewsPage(page)

        with allure.step('Открыть первую новость из списка'):
            news_page.open_list()
            news_page.open_news(news_page.get_first_news_title())

        with allure.step('Собрать автора и дату'):
            author = news_page.get_author()
            date = news_page.get_date()

        with allure.step('Проверить, что автор и дата непустые'):
            soft_assertions.check(bool(author), 'Автор не отображается на странице новости')
            soft_assertions.check(bool(date), 'Дата не отображается на странице новости')
            soft_assertions.assert_all()
