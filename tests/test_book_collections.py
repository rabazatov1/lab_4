import pytest
from src.book import Book
from src.book_collections import BookCollection, IndexDict


@pytest.fixture
def sample_books():
    return [
        Book("Война и мир", "Лев Толстой", 1869, "Роман", "978-1"),
        Book("Анна Каренина", "Лев Толстой", 1877, "Роман", "978-2"),
        Book("Мастер и Маргарита", "Михаил Булгаков", 1967, "Фантастика", "978-3"),
        Book("Идиот", "Фёдор Достоевский", 1869, "Роман", "978-4"),
    ]


@pytest.fixture
def empty_collection():
    return BookCollection()


@pytest.fixture
def filled_collection(sample_books):
    return BookCollection(sample_books)


class TestBookCollectionCreation:
    def test_creation_empty(self, empty_collection):
        assert len(empty_collection) == 0

    def test_creation_with_list(self, sample_books):
        collection = BookCollection(sample_books)
        assert len(collection) == 4

    def test_creation_with_invalid_data_int(self):
        with pytest.raises(TypeError) as exc_info:
            BookCollection(12345)
        assert "итерируемым объектом" in str(exc_info.value)


class TestBookCollectionIndexing:
    def test_getitem_by_index_normal(self, filled_collection, sample_books):
        assert filled_collection[0] == sample_books[0]
        assert filled_collection[-1] == sample_books[-1]

    def test_getitem_by_slice(self, filled_collection, sample_books):
        sliced = filled_collection[1:3]
        assert isinstance(sliced, BookCollection)
        assert len(sliced) == 2

    def test_getitem_out_of_range(self, filled_collection):
        with pytest.raises(IndexError):
            _ = filled_collection[10]

    def test_getitem_invalid_type(self, filled_collection):
        with pytest.raises(TypeError):
            _ = filled_collection["некорректно"]


class TestBookCollectionAddition:
    def test_add_two_collections(self, sample_books):
        col1 = BookCollection(sample_books[:2])
        col2 = BookCollection(sample_books[2:])
        result = col1 + col2
        assert isinstance(result, BookCollection)
        assert len(result) == 4

    def test_add_invalid_type(self, filled_collection):
        with pytest.raises(TypeError):
            _ = filled_collection + "некорректно"


class TestBookCollectionMethods:
    def test_add_book(self, empty_collection, sample_books):
        empty_collection.add(sample_books[0])
        assert len(empty_collection) == 1
        assert sample_books[0] in empty_collection

    def test_remove_book(self, filled_collection, sample_books):
        filled_collection.remove(sample_books[0])
        assert len(filled_collection) == 3
        assert sample_books[0] not in filled_collection


class TestBookCollectionContains:
    def test_contains_existing_book(self, filled_collection, sample_books):
        assert sample_books[0] in filled_collection

    def test_contains_nonexistent_book(self, filled_collection):
        nonexistent = Book("Несуществующая", "Неизвестный", 2000, "Фантастика", "999")
        assert nonexistent not in filled_collection


class TestIndexDictCreation:
    def test_creation_empty(self):
        index = IndexDict()
        assert len(index) == 0

    def test_creation_with_books(self, sample_books):
        index = IndexDict(sample_books)
        assert len(index) == 4

    def test_creation_with_invalid_book_type(self):
        with pytest.raises(TypeError) as exc_info:
            IndexDict([None, "строка", 123])
        assert "Ожидался объект Book" in str(exc_info.value)


class TestIndexDictGetItem:
    def test_getitem_by_isbn(self, sample_books):
        index = IndexDict(sample_books)
        book = index["isbn", "978-1"]
        assert book == sample_books[0]

    def test_getitem_by_author(self, sample_books):
        index = IndexDict(sample_books)
        results = index["author", "Лев Толстой"]
        assert isinstance(results, BookCollection)
        assert len(results) == 2

    def test_getitem_by_year(self, sample_books):
        index = IndexDict(sample_books)
        results = index["year", 1869]
        assert isinstance(results, BookCollection)
        assert len(results) == 2

    def test_getitem_nonexistent_isbn(self, sample_books):
        index = IndexDict(sample_books)
        result = index["isbn", "999-999"]
        assert result is None

    def test_getitem_invalid_index_type(self, sample_books):
        index = IndexDict(sample_books)
        with pytest.raises(KeyError):
            _ = index["некорректный_тип", "значение"]

    def test_getitem_not_tuple(self, sample_books):
        index = IndexDict(sample_books)
        with pytest.raises(TypeError):
            _ = index["isbn"]


class TestIndexDictMethods:
    def test_add_book(self, sample_books):
        index = IndexDict()
        index.add_book(sample_books[0])
        assert len(index) == 1
        assert index["isbn", "978-1"] == sample_books[0]

    def test_add_multiple_books_same_author(self, sample_books):
        index = IndexDict()
        index.add_book(sample_books[0])
        index.add_book(sample_books[1])
        results = index["author", "Лев Толстой"]
        assert len(results) == 2

    def test_remove_book(self, sample_books):
        index = IndexDict(sample_books)
        index.remove_book(sample_books[0])
        assert len(index) == 3
        assert index["isbn", "978-1"] is None

    def test_remove_book_cleans_empty_indices(self, sample_books):
        index = IndexDict([sample_books[2]])
        index.remove_book(sample_books[2])
        results = index["author", "Михаил Булгаков"]
        assert len(results) == 0


class TestIndexDictContains:
    def test_contains_book_object(self, sample_books):
        index = IndexDict(sample_books)
        assert sample_books[0] in index

    def test_contains_isbn_string(self, sample_books):
        index = IndexDict(sample_books)
        assert "978-1" in index

    def test_not_contains_book(self, sample_books):
        index = IndexDict(sample_books)
        nonexistent = Book("Несуществующая", "Неизвестный", 2000, "Фантастика", "999")
        assert nonexistent not in index


class TestBookCollectionStr:
    def test_str_empty_collection(self):
        collection = BookCollection()
        assert str(collection) == "Количество книг: 0"

    def test_str_filled_collection(self, sample_books):
        collection = BookCollection(sample_books)
        assert str(collection) == "Количество книг: 4"


class TestIndexDictStr:
    def test_str_empty_index(self):
        index = IndexDict()
        assert str(index) == "Количество уникальных книг: 0"

    def test_str_filled_index(self, sample_books):
        index = IndexDict(sample_books)
        assert str(index) == "Количество уникальных книг: 4"


class TestBookCollectionEquality:
    def test_equality_same_books_same_order(self, sample_books):
        col1 = BookCollection(sample_books[:3])
        col2 = BookCollection(sample_books[:3])
        assert col1 == col2

    def test_equality_different_books(self, sample_books):
        col1 = BookCollection(sample_books[:2])
        col2 = BookCollection(sample_books[2:4])
        assert col1 != col2
