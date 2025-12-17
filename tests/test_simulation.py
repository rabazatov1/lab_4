import pytest
from io import StringIO
from unittest.mock import patch, MagicMock
from src.simulation import (
    run_simulation,
    _event_add_book,
    _event_remove_book,
    _event_search_by_author,
    _event_search_by_genre,
    _event_search_by_year,
    _event_search_nonexistent,
)
from src.library import Library
from src.book import Book


@pytest.fixture
def sample_books():
    return [
        Book("Война и мир", "Лев Толстой", 1869, "Роман", "978-1"),
        Book("Анна Каренина", "Лев Толстой", 1877, "Роман", "978-2"),
        Book("Мастер и Маргарита", "Михаил Булгаков", 1967, "Фантастика", "978-3"),
    ]


@pytest.fixture
def library_with_books(sample_books):
    library = Library()
    for book in sample_books[:2]:
        library.add_book(book)
    return library


class TestEventAddBook:
    def test_add_book_normal(self, library_with_books, sample_books):
        initial_count = len(library_with_books.books)
        _event_add_book(library_with_books, sample_books)
        assert len(library_with_books.books) >= initial_count

    def test_add_book_empty_library(self, sample_books):
        library = Library()
        _event_add_book(library, sample_books)
        assert len(library.books) == 1

    def test_add_book_all_books_present(self, library_with_books, sample_books):
        for book in sample_books:
            if book not in library_with_books.books:
                library_with_books.add_book(book)

        initial_count = len(library_with_books.books)
        _event_add_book(library_with_books, sample_books)
        assert len(library_with_books.books) == initial_count

    def test_add_book_empty_available_list(self):
        library = Library()
        _event_add_book(library, [])
        assert len(library.books) == 0


class TestEventRemoveBook:
    def test_remove_book_normal(self, library_with_books):
        initial_count = len(library_with_books.books)
        _event_remove_book(library_with_books)
        assert len(library_with_books.books) == initial_count - 1

    def test_remove_book_empty_library(self):
        library = Library()
        _event_remove_book(library)
        assert len(library.books) == 0

    def test_remove_book_single_book(self, sample_books):
        library = Library()
        library.add_book(sample_books[0])
        _event_remove_book(library)
        assert len(library.books) == 0


class TestEventSearchByAuthor:
    def test_search_by_author_found(self, library_with_books):
        with patch('src.simulation.AUTHORS', ['Лев Толстой']):
            _event_search_by_author(library_with_books)

    def test_search_by_author_not_found(self, library_with_books):
        with patch('src.simulation.AUTHORS', ['Неизвестный Автор']):
            _event_search_by_author(library_with_books)

    def test_search_by_author_empty_library(self):
        library = Library()
        with patch('src.simulation.AUTHORS', ['Лев Толстой']):
            _event_search_by_author(library)


class TestEventSearchByGenre:
    def test_search_by_genre_found(self, library_with_books):
        with patch('src.simulation.GENRES', ['Роман']):
            _event_search_by_genre(library_with_books)

    def test_search_by_genre_not_found(self, library_with_books):
        with patch('src.simulation.GENRES', ['Детектив']):
            _event_search_by_genre(library_with_books)

    def test_search_by_genre_empty_library(self):
        library = Library()
        with patch('src.simulation.GENRES', ['Роман']):
            _event_search_by_genre(library)


class TestEventSearchByYear:
    def test_search_by_year_found(self, library_with_books):
        with patch('src.simulation.YEARS', [1869]):
            _event_search_by_year(library_with_books)

    def test_search_by_year_not_found(self, library_with_books):
        with patch('src.simulation.YEARS', [2999]):
            _event_search_by_year(library_with_books)

    def test_search_by_year_empty_library(self):
        library = Library()
        with patch('src.simulation.YEARS', [1869]):
            _event_search_by_year(library)


class TestEventSearchNonexistent:
    def test_search_nonexistent_isbn(self, library_with_books):
        with patch('src.simulation.FAKE_ISBNS', ['999-999']):
            _event_search_nonexistent(library_with_books)

    def test_search_nonexistent_empty_library(self):
        library = Library()
        with patch('src.simulation.FAKE_ISBNS', ['999-999']):
            _event_search_nonexistent(library)


class TestRunSimulation:
    @patch('src.simulation.create_sample_books')
    def test_run_simulation_normal(self, mock_create_books, sample_books):
        mock_create_books.return_value = sample_books
        run_simulation(steps=5, seed=42)

    @patch('src.simulation.create_sample_books')
    def test_run_simulation_with_seed(self, mock_create_books, sample_books):
        mock_create_books.return_value = sample_books

        output1 = StringIO()
        with patch('sys.stdout', output1):
            run_simulation(steps=3, seed=42)

        output2 = StringIO()
        with patch('sys.stdout', output2):
            run_simulation(steps=3, seed=42)

        assert output1.getvalue() == output2.getvalue()

    @patch('src.simulation.create_sample_books')
    def test_run_simulation_without_seed(self, mock_create_books, sample_books):
        mock_create_books.return_value = sample_books
        run_simulation(steps=5, seed=None)

    @patch('src.simulation.create_sample_books')
    def test_run_simulation_zero_steps(self, mock_create_books, sample_books):
        mock_create_books.return_value = sample_books
        run_simulation(steps=0, seed=42)

    @patch('src.simulation.create_sample_books')
    def test_run_simulation_one_step(self, mock_create_books, sample_books):
        mock_create_books.return_value = sample_books
        run_simulation(steps=1, seed=42)

    @patch('src.simulation.create_sample_books')
    def test_run_simulation_many_steps(self, mock_create_books, sample_books):
        mock_create_books.return_value = sample_books
        run_simulation(steps=100, seed=42)

    @patch('src.simulation.create_sample_books')
    def test_run_simulation_error_handling(self, mock_create_books):
        mock_create_books.return_value = []
        run_simulation(steps=5, seed=42)

    @patch('src.simulation.create_sample_books')
    def test_run_simulation_prints_output(self, mock_create_books, sample_books):
        mock_create_books.return_value = sample_books

        output = StringIO()
        with patch('sys.stdout', output):
            run_simulation(steps=2, seed=42)

        output_text = output.getvalue()
        assert "ПСЕВДОСЛУЧАЙНАЯ СИМУЛЯЦИЯ" in output_text
        assert "ФИНАЛЬНОЕ СОСТОЯНИЕ" in output_text
        assert "Шаг" in output_text


class TestSimulationIntegration:
    @patch('src.simulation.create_sample_books')
    def test_simulation_all_events(self, mock_create_books, sample_books):
        extended_books = []
        for i in range(50):
            book = Book(f"Тестовая книга {i}", f"Автор {i % 10}", 2000 + i % 20, "Жанр", f"ISBN-TEST-{i}")
            extended_books.append(book)
        mock_create_books.return_value = extended_books

        output = StringIO()
        with patch('sys.stdout', output):
            run_simulation(steps=50, seed=42)

        output_text = output.getvalue()
        assert "Событие:" in output_text

    @patch('src.simulation.create_sample_books')
    def test_simulation_reproducibility(self, mock_create_books, sample_books):
        unique_books = []
        for i in range(30):
            book = Book(f"Книга {i}", f"Автор {i % 5}", 2000 + i, "Жанр", f"ISBN-UNIQUE-{i}")
            unique_books.append(book)
        mock_create_books.return_value = unique_books

        output1 = StringIO()
        with patch('sys.stdout', output1):
            run_simulation(steps=10, seed=123)

        unique_books_copy = []
        for i in range(30):
            book = Book(f"Книга {i}", f"Автор {i % 5}", 2000 + i, "Жанр", f"ISBN-UNIQUE-{i}")
            unique_books_copy.append(book)
        mock_create_books.return_value = unique_books_copy
        output2 = StringIO()
        with patch('sys.stdout', output2):
            run_simulation(steps=10, seed=123)

        assert output1.getvalue() == output2.getvalue()

    @patch('src.simulation.create_sample_books')
    def test_simulation_randomness_without_seed(self, mock_create_books, sample_books):
        unique_books = []
        for i in range(30):
            book = Book(f"Книга {i}", f"Автор {i % 5}", 2000 + i, "Жанр", f"ISBN-RANDOM-{i}")
            unique_books.append(book)
        mock_create_books.return_value = unique_books

        output1 = StringIO()
        with patch('sys.stdout', output1):
            run_simulation(steps=10, seed=None)

        unique_books_copy = []
        for i in range(30):
            book = Book(f"Книга {i}", f"Автор {i % 5}", 2000 + i, "Жанр", f"ISBN-RANDOM-{i}")
            unique_books_copy.append(book)
        mock_create_books.return_value = unique_books_copy
        output2 = StringIO()
        with patch('sys.stdout', output2):
            run_simulation(steps=10, seed=None)

        assert len(output1.getvalue()) > 0
        assert len(output2.getvalue()) > 0
