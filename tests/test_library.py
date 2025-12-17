import pytest
from src.book import Book
from src.book_collections import BookCollection
from src.library import Library


@pytest.fixture
def sample_books():
    return [
        Book("Война и мир", "Лев Толстой", 1869, "Роман", "978-1"),
        Book("Анна Каренина", "Лев Толстой", 1877, "Роман", "978-2"),
        Book("Мастер и Маргарита", "Михаил Булгаков", 1967, "Фантастика", "978-3"),
        Book("Преступление и наказание", "Фёдор Достоевский", 1866, "Роман", "978-4"),
        Book("Евгений Онегин", "Александр Пушкин", 1833, "Поэма", "978-5"),
    ]


@pytest.fixture
def empty_library():
    return Library()


@pytest.fixture
def filled_library(sample_books):
    library = Library()
    for book in sample_books:
        library.add_book(book)
    return library


class TestLibraryCreation:
    def test_creation_empty(self, empty_library):
        assert len(empty_library.books) == 0
        assert len(empty_library.indexes) == 0

    def test_creation_with_books(self, sample_books):
        collection = BookCollection(sample_books)
        library = Library(books=collection)
        assert len(library.books) == 5
        assert len(library.indexes) == 5


class TestLibraryAddBook:
    def test_add_single_book(self, empty_library, sample_books):
        empty_library.add_book(sample_books[0])
        assert len(empty_library.books) == 1
        assert len(empty_library.indexes) == 1
        assert sample_books[0] in empty_library.books

    def test_add_multiple_books(self, empty_library, sample_books):
        for book in sample_books:
            empty_library.add_book(book)
        assert len(empty_library.books) == 5
        assert len(empty_library.indexes) == 5

    def test_add_duplicate_book(self, empty_library, sample_books):
        empty_library.add_book(sample_books[0])
        with pytest.raises(ValueError) as exc_info:
            empty_library.add_book(sample_books[0])
        assert "уже существует" in str(exc_info.value)
        assert len(empty_library.books) == 1
        assert len(empty_library.indexes) == 1


class TestLibraryRemoveBook:
    def test_remove_existing_book(self, filled_library, sample_books):
        filled_library.remove_book(sample_books[0])
        assert len(filled_library.books) == 4
        assert len(filled_library.indexes) == 4
        assert sample_books[0] not in filled_library.books

    def test_remove_all_books(self, filled_library, sample_books):
        for book in sample_books:
            filled_library.remove_book(book)
        assert len(filled_library.books) == 0
        assert len(filled_library.indexes) == 0

    def test_remove_nonexistent_book(self, filled_library):
        nonexistent = Book("Несуществующая", "Неизвестный", 2000, "Фантастика", "999")
        initial_count = len(filled_library.books)
        filled_library.remove_book(nonexistent)
        assert len(filled_library.books) == initial_count


class TestLibrarySearchByISBN:
    def test_search_existing_isbn(self, filled_library, sample_books):
        result = filled_library.search_by_isbn("978-1")
        assert result == sample_books[0]

    def test_search_nonexistent_isbn(self, filled_library):
        result = filled_library.search_by_isbn("999-999")
        assert result is None

    def test_search_isbn_in_empty_library(self, empty_library):
        result = empty_library.search_by_isbn("978-1")
        assert result is None

    def test_search_empty_isbn(self, filled_library):
        result = filled_library.search_by_isbn("")
        assert result is None


class TestLibrarySearchByAuthor:
    def test_search_existing_author(self, filled_library):
        results = filled_library.search_by_author("Лев Толстой")
        assert isinstance(results, BookCollection)
        assert len(results) == 2

    def test_search_nonexistent_author(self, filled_library):
        results = filled_library.search_by_author("Неизвестный Автор")
        assert isinstance(results, BookCollection)
        assert len(results) == 0

    def test_search_author_in_empty_library(self, empty_library):
        results = empty_library.search_by_author("Лев Толстой")
        assert isinstance(results, BookCollection)
        assert len(results) == 0

    def test_search_author_case_sensitive(self, filled_library):
        results = filled_library.search_by_author("лев толстой")
        assert len(results) == 0


class TestLibrarySearchByYear:
    def test_search_existing_year(self, filled_library):
        results = filled_library.search_by_year(1869)
        assert isinstance(results, BookCollection)
        assert len(results) == 1

    def test_search_year_multiple_books(self, filled_library, sample_books):
        extra_book = Book("Ещё одна книга 1869", "Автор", 1869, "Роман", "978-10")
        filled_library.add_book(extra_book)
        results = filled_library.search_by_year(1869)
        assert len(results) == 2

    def test_search_nonexistent_year(self, filled_library):
        results = filled_library.search_by_year(2999)
        assert isinstance(results, BookCollection)
        assert len(results) == 0

    def test_search_year_zero(self, filled_library):
        results = filled_library.search_by_year(0)
        assert len(results) == 0

    def test_search_negative_year(self, filled_library):
        results = filled_library.search_by_year(-1000)
        assert len(results) == 0


class TestLibrarySearchByGenre:
    def test_search_existing_genre(self, filled_library):
        results = filled_library.search_by_genre("Роман")
        assert isinstance(results, BookCollection)
        assert len(results) == 3

    def test_search_nonexistent_genre(self, filled_library):
        results = filled_library.search_by_genre("Детектив")
        assert isinstance(results, BookCollection)
        assert len(results) == 0

    def test_search_genre_in_empty_library(self, empty_library):
        results = empty_library.search_by_genre("Роман")
        assert len(results) == 0

    def test_search_genre_case_sensitive(self, filled_library):
        results = filled_library.search_by_genre("роман")
        assert len(results) == 0


class TestLibraryGetRandomBook:
    def test_get_random_from_filled_library(self, filled_library, sample_books):
        book = filled_library.get_random_book()
        assert book is not None
        assert book in sample_books

    def test_get_random_from_empty_library(self, empty_library):
        book = empty_library.get_random_book()
        assert book is None

    def test_get_random_from_single_book_library(self, empty_library, sample_books):
        empty_library.add_book(sample_books[0])
        book = empty_library.get_random_book()
        assert book == sample_books[0]

    def test_get_random_multiple_times(self, filled_library):
        books = set()
        for _ in range(20):
            book = filled_library.get_random_book()
            books.add(book.isbn)
        assert len(books) >= 1


class TestLibraryStr:
    def test_str_empty_library(self, empty_library):
        result = str(empty_library)
        assert "Общее количество книг: 0" in result
        assert "количество уникальных книг: 0" in result

    def test_str_filled_library(self, filled_library):
        result = str(filled_library)
        assert "Общее количество книг: 5" in result
        assert "количество уникальных книг: 5" in result

    def test_str_format(self, empty_library, sample_books):
        empty_library.add_book(sample_books[0])
        empty_library.add_book(sample_books[1])
        result = str(empty_library)
        expected = "Общее количество книг: 2, количество уникальных книг: 2"
        assert result == expected


class TestLibraryIntegration:
    def test_add_search_remove_workflow(self, empty_library, sample_books):
        empty_library.add_book(sample_books[0])
        empty_library.add_book(sample_books[1])

        result = empty_library.search_by_isbn("978-1")
        assert result == sample_books[0]

        author_books = empty_library.search_by_author("Лев Толстой")
        assert len(author_books) == 2

        empty_library.remove_book(sample_books[0])
        result = empty_library.search_by_isbn("978-1")
        assert result is None

        author_books = empty_library.search_by_author("Лев Толстой")
        assert len(author_books) == 1

    def test_sync_between_books_and_indexes(self, empty_library, sample_books):
        for book in sample_books:
            empty_library.add_book(book)

        assert len(empty_library.books) == len(empty_library.indexes)

        for book in sample_books[:3]:
            empty_library.remove_book(book)

        assert len(empty_library.books) == len(empty_library.indexes)
        assert len(empty_library.books) == 2
