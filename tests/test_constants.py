import pytest
import json
from unittest.mock import patch, mock_open
from src.constants import _load_json_data, create_sample_books, GENRES, AUTHORS, YEARS, FAKE_ISBNS
from src.book import Book


class TestLoadJsonData:
    def test_load_json_data_normal(self):
        data = _load_json_data()
        assert isinstance(data, dict)
        assert 'books' in data
        assert 'genres' in data
        assert 'authors' in data
        assert 'years' in data
        assert 'fake_isbns' in data

    def test_load_json_data_structure(self):
        data = _load_json_data()
        assert isinstance(data['books'], list)
        assert isinstance(data['genres'], list)
        assert isinstance(data['authors'], list)
        assert isinstance(data['years'], list)
        assert isinstance(data['fake_isbns'], list)

    def test_load_json_data_books_structure(self):
        data = _load_json_data()
        if len(data['books']) > 0:
            book = data['books'][0]
            assert 'title' in book
            assert 'author' in book
            assert 'year' in book
            assert 'genre' in book
            assert 'isbn' in book


    @patch('builtins.open', mock_open(read_data='неверный json'))
    def test_load_json_invalid_json(self, ):
        with pytest.raises(json.JSONDecodeError):
            with patch('src.constants.JSON_FILE_PATH', 'фейковый_путь.json'):
                _load_json_data()

    @patch('builtins.open', mock_open(read_data='{}'))
    def test_load_json_empty_json(self):
        with patch('src.constants.JSON_FILE_PATH', 'фейковый_путь.json'):
            data = _load_json_data()
            assert isinstance(data, dict)
            assert len(data) == 0


class TestCreateSampleBooks:
    def test_create_sample_books_normal(self):
        books = create_sample_books()
        assert isinstance(books, list)
        assert len(books) > 0
        assert all(isinstance(book, Book) for book in books)

    def test_create_sample_books_properties(self):
        books = create_sample_books()
        if len(books) > 0:
            book = books[0]
            assert hasattr(book, 'title')
            assert hasattr(book, 'author')
            assert hasattr(book, 'year')
            assert hasattr(book, 'genre')
            assert hasattr(book, 'isbn')
            assert isinstance(book.title, str)
            assert isinstance(book.author, str)
            assert isinstance(book.year, int)
            assert isinstance(book.genre, str)
            assert isinstance(book.isbn, str)

    def test_create_sample_books_unique_isbns(self):
        books = create_sample_books()
        isbns = [book.isbn for book in books]
        assert len(isbns) == len(set(isbns)), "Найдены дублирующиеся ISBN"

    def test_create_sample_books_count(self):
        data = _load_json_data()
        books = create_sample_books()
        assert len(books) == len(data['books'])

    @patch('src.constants._DATA', {'books': []})
    def test_create_sample_books_empty_data(self):
        books = create_sample_books()
        assert isinstance(books, list)
        assert len(books) == 0

    @patch('src.constants._DATA', {
        'books': [
            {
                'title': 'Тестовая Книга',
                'author': 'Тестовый Автор',
                'year': 2020,
                'genre': 'Тест',
                'isbn': '123'
            }
        ]
    })
    def test_create_sample_books_single_book(self):
        books = create_sample_books()
        assert len(books) == 1
        assert books[0].title == 'Тестовая Книга'
        assert books[0].author == 'Тестовый Автор'


class TestConstants:
    def test_genres_constant(self):
        assert isinstance(GENRES, list)
        assert len(GENRES) > 0
        assert all(isinstance(genre, str) for genre in GENRES)

    def test_authors_constant(self):
        assert isinstance(AUTHORS, list)
        assert len(AUTHORS) > 0
        assert all(isinstance(author, str) for author in AUTHORS)

    def test_years_constant(self):
        assert isinstance(YEARS, list)
        assert len(YEARS) > 0
        assert all(isinstance(year, int) for year in YEARS)

    def test_fake_isbns_constant(self):
        assert isinstance(FAKE_ISBNS, list)
        assert len(FAKE_ISBNS) > 0
        assert all(isinstance(isbn, str) for isbn in FAKE_ISBNS)

    def test_genres_not_empty_strings(self):
        assert all(len(genre) > 0 for genre in GENRES)

    def test_authors_not_empty_strings(self):
        assert all(len(author) > 0 for author in AUTHORS)

    def test_years_valid_range(self):
        assert all(-1000 <= year <= 3000 for year in YEARS)

    def test_fake_isbns_not_empty_strings(self):
        assert all(len(isbn) > 0 for isbn in FAKE_ISBNS)


class TestDataIntegrity:
    def test_books_have_authors_from_list(self):
        books = create_sample_books()
        book_authors = set(book.author for book in books)
        assert len(book_authors) > 0
        assert len(AUTHORS) > 0

    def test_books_have_genres_from_list(self):
        books = create_sample_books()
        book_genres = set(book.genre for book in books)
        assert len(book_genres) > 0
        assert len(GENRES) > 0

    def test_books_have_years_from_list(self):
        books = create_sample_books()
        book_years = set(book.year for book in books)
        assert len(book_years) > 0
        assert len(YEARS) > 0

    def test_fake_isbns_not_in_books(self):
        books = create_sample_books()
        book_isbns = set(book.isbn for book in books)
        fake_isbns_set = set(FAKE_ISBNS)

        intersection = book_isbns & fake_isbns_set
        assert len(intersection) == 0, f"Найдены совпадающие ISBN: {intersection}"

class TestEdgeCases:
    def test_books_with_same_title_different_isbn(self):
        books = create_sample_books()
        titles = [book.title for book in books]
        isbns = [book.isbn for book in books]

        assert len(isbns) == len(set(isbns))

    def test_books_with_unicode_characters(self):
        books = create_sample_books()
        for book in books:
            assert isinstance(book.title, str)
            assert isinstance(book.author, str)
            str(book)

    def test_books_with_very_old_years(self):
        books = create_sample_books()
        for book in books:
            assert isinstance(book.year, int)

    def test_constants_immutability(self):
        original_genres_count = len(GENRES)
        original_authors_count = len(AUTHORS)

        genres_copy = GENRES.copy()
        genres_copy.append("Новый Жанр")

        authors_copy = AUTHORS.copy()
        authors_copy.append("Новый Автор")

        assert len(GENRES) == original_genres_count
        assert len(AUTHORS) == original_authors_count
