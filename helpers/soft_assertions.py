class SoftAssertions:
    """Сборщик ошибок: накапливает все невыполненные проверки
    и выбрасывает AssertionError со всеми сообщениями разом."""

    def __init__(self):
        self.errors = []

    def check(self, condition, message):
        if not condition:
            self.errors.append(message)

    def assert_all(self):
        if self.errors:
            raise AssertionError(
                '\n'.join(self.errors)
            )