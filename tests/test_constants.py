from src.constants import _load_json_data, create_sample_books, GENRES, AUTHORS, YEARS, FAKE_ISBNS
from src.book import Book


class TestLoadJsonData:
    def test_load_json_data_normal(self):
        data = _load_json_data()
        assert isinstance(data, dict)
        assert "books" in data
        assert "genres" in data
        assert "authors" in data

    def test_load_json_data_structure(self):
        data = _load_json_data()
        assert isinstance(data["books"], list)
        assert isinstance(data["genres"], list)


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
            assert hasattr(book, "title")
            assert hasattr(book, "author")
            assert isinstance(book.title, str)
            assert isinstance(book.year, int)

    def test_create_sample_books_unique_isbns(self):
        books = create_sample_books()
        isbns = [book.isbn for book in books]
        assert len(isbns) == len(set(isbns)), "Найдены дублирующиеся ISBN"


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

    def test_fake_isbns_not_in_books(self):
        books = create_sample_books()
        book_isbns = set(book.isbn for book in books)
        fake_isbns_set = set(FAKE_ISBNS)

        intersection = book_isbns & fake_isbns_set
        assert len(intersection) == 0, f"Найдены совпадающие ISBN: {intersection}"
