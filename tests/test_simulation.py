import pytest
from io import StringIO
from unittest.mock import patch
from src.simulation import (
    run_simulation,
    _event_add_book,
    _event_remove_book,
    _event_search_by_author,
    _event_search_by_genre,
    _event_search_by_year,
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


class TestEventRemoveBook:
    def test_remove_book_normal(self, library_with_books):
        initial_count = len(library_with_books.books)
        _event_remove_book(library_with_books)
        assert len(library_with_books.books) == initial_count - 1

    def test_remove_book_empty_library(self):
        library = Library()
        _event_remove_book(library)
        assert len(library.books) == 0


class TestEventSearchByAuthor:
    def test_search_by_author_found(self, library_with_books):
        with patch("src.simulation.AUTHORS", ["Лев Толстой"]):
            _event_search_by_author(library_with_books)


class TestEventSearchByGenre:
    def test_search_by_genre_found(self, library_with_books):
        with patch("src.simulation.GENRES", ["Роман"]):
            _event_search_by_genre(library_with_books)


class TestEventSearchByYear:
    def test_search_by_year_found(self, library_with_books):
        with patch("src.simulation.YEARS", [1869]):
            _event_search_by_year(library_with_books)


class TestRunSimulation:
    @patch("src.simulation.create_sample_books")
    def test_run_simulation_normal(self, mock_create_books, sample_books):
        mock_create_books.return_value = sample_books
        run_simulation(steps=5, seed=42)

    @patch("src.simulation.create_sample_books")
    def test_run_simulation_with_seed(self, mock_create_books, sample_books):
        mock_create_books.return_value = sample_books

        output1 = StringIO()
        with patch("sys.stdout", output1):
            run_simulation(steps=3, seed=42)

        output2 = StringIO()
        with patch("sys.stdout", output2):
            run_simulation(steps=3, seed=42)

        assert output1.getvalue() == output2.getvalue()

    @patch("src.simulation.create_sample_books")
    def test_run_simulation_prints_output(self, mock_create_books, sample_books):
        mock_create_books.return_value = sample_books

        output = StringIO()
        with patch("sys.stdout", output):
            run_simulation(steps=2, seed=42)

        output_text = output.getvalue()
        assert "ПСЕВДОСЛУЧАЙНАЯ СИМУЛЯЦИЯ" in output_text
        assert "ФИНАЛЬНОЕ СОСТОЯНИЕ" in output_text
