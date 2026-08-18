import allure

from pages.pagination_page import PaginationPage


@allure.epic('Новости')
@allure.feature('Пагинация')
class TestPagination:
    @allure.story('Переход на 2-ю страницу и возврат на 1-ю')
    @allure.severity(allure.severity_level.NORMAL)
    @allure.description(
        'SPA-пагинация: клик «2» меняет контент без смены URL, '
        'возврат на 1-ю страницу восстанавливает исходный контент.'
    )
    def test_pagination_navigation(self, page):
        """Переход на 2-ю страницу списка новостей и возврат на 1-ю.

        URL при пагинации не меняется (SPA), поэтому переход проверяется
        по изменению активной кнопки и содержимого списка.
        """
        pagination_page = PaginationPage(page)

        with allure.step('Открыть список новостей'):
            pagination_page.open()

        with allure.step('Убедиться, что вторая страница существует, иначе skip'):
            if not pagination_page.has_page_button(2):
                import pytest
                pytest.skip('На сайте нет второй страницы новостей — пагинация недоступна')

        first_page_title = pagination_page.get_first_news_title()

        with allure.step('Перейти на вторую страницу'):
            pagination_page.go_to_page(2)
            pagination_page.wait_active_page(2)

        second_page_title = pagination_page.get_first_news_title()

        with allure.step('Проверить, что контент изменился'):
            assert first_page_title != second_page_title, (
                f'Контент не изменился при переходе на 2-ю страницу: '
                f'первый заголовок "{first_page_title}"'
            )

        with allure.step('Вернуться на первую страницу'):
            pagination_page.go_to_previous()
            pagination_page.wait_active_page(1)

        with allure.step('Проверить, что исходный контент восстановился'):
            pagination_page.wait_first_news_title(first_page_title)
