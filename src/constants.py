import json
import os
from typing import List
from src.book import Book

JSON_FILE_PATH = os.path.join(os.path.dirname(__file__), 'books_data.json')


def _load_json_data() -> dict:
    """
    Загружает данные из JSON файла

    :return: Словарь с данными из JSON
    :rtype: dict
    """
    with open(JSON_FILE_PATH, 'r', encoding='utf-8') as file:
        return json.load(file)


_DATA = _load_json_data()

BOOK_DATA = [
    (book['title'], book['author'], book['year'], book['genre'], book['isbn'])
    for book in _DATA['books']
]

GENRES = _DATA['genres']
AUTHORS = _DATA['authors']
YEARS = _DATA['years']
FAKE_ISBNS = _DATA['fake_isbns']


def create_sample_books() -> List[Book]:
    """
    Создаёт список книг из данных JSON

    :return: Список объектов Book
    :rtype: List[Book]
    """
    return [
        Book(book['title'], book['author'], book['year'], book['genre'], book['isbn'])
        for book in _DATA['books']
    ]
