import requests

API_BASE_URL = 'https://archiscope.ru'


class APIClient:
    """Клиент для API-предусловий (FastAPI archiscope.ru)."""

    def __init__(self, base_url=API_BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()

    def register(self, user_data):
        return self.session.post(
            f'{self.base_url}/api/auth/register',
            json=user_data,
        )

    def login(self, email, password):
        return self.session.post(
            f'{self.base_url}/api/auth/login',
            data={'username': email, 'password': password},
        )

    def get_me(self, token):
        return self.session.get(
            f'{self.base_url}/api/users/me',
            headers={'Authorization': f'Bearer {token}'},
        )

    def get_news(self, page=1, per_page=10):
        return self.session.get(
            f'{self.base_url}/api/news/',
            params={'page': page, 'per_page': per_page},
        )

    def create_news(self, token, news_data):
        return self.session.post(
            f'{self.base_url}/api/news/',
            headers={'Authorization': f'Bearer {token}'},
            json=news_data,
        )

    def cleanup_user(self, email):
        """Удаление пользователя. Эндпоинт может отсутствовать —
        при 404/405 считаем, что чистка не предусмотрена бэкендом."""
        resp = self.session.delete(
            f'{self.base_url}/api/users/by_email/{email}',
        )
        return resp.status_code in (200, 204, 404, 405)