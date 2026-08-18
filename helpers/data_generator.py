import random
from faker import Faker

fake = Faker('ru_RU')


def generate_user():
    return {
        'email': fake.email(),
        'password': fake.password(length=12),
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'phone': fake.phone_number(),
    }


def generate_news():
    return {
        'title': fake.sentence(nb_words=4, variable_nb_words=True)[:-1],
        'subtitle': fake.sentence(nb_words=6, variable_nb_words=True)[:-1],
        'text': fake.paragraph(nb_sentences=4),
        'tags': ', '.join(fake.words(nb=3)),
    }


def generate_comment():
    return fake.sentence(nb_words=8, variable_nb_words=True)[:-1]