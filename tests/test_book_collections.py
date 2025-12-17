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

    def test_creation_with_none(self):
        collection = BookCollection(None)
        assert len(collection) == 0

    def test_creation_with_invalid_data_int(self):
        with pytest.raises(TypeError) as exc_info:
            BookCollection(12345)
        assert "итерируемым объектом" in str(exc_info.value)

    def test_creation_with_invalid_data_string(self):
        collection = BookCollection("строка")
        assert len(collection) == 6

    def test_creation_with_invalid_data_dict(self):
        collection = BookCollection({"ключ": "значение"})
        assert len(collection) == 1


class TestBookCollectionIteration:
    def test_iteration_normal(self, filled_collection, sample_books):
        books_list = list(filled_collection)
        assert len(books_list) == len(sample_books)
        assert books_list == sample_books

    def test_iteration_empty(self, empty_collection):
        books_list = list(empty_collection)
        assert books_list == []


class TestBookCollectionIndexing:
    def test_getitem_by_index_normal(self, filled_collection, sample_books):
        assert filled_collection[0] == sample_books[0]
        assert filled_collection[1] == sample_books[1]
        assert filled_collection[-1] == sample_books[-1]

    def test_getitem_by_slice(self, filled_collection, sample_books):
        sliced = filled_collection[1:3]
        assert isinstance(sliced, BookCollection)
        assert len(sliced) == 2
        assert list(sliced) == sample_books[1:3]

    def test_getitem_slice_empty(self, filled_collection):
        sliced = filled_collection[2:2]
        assert isinstance(sliced, BookCollection)
        assert len(sliced) == 0

    def test_getitem_out_of_range(self, filled_collection):
        with pytest.raises(IndexError):
            _ = filled_collection[10]

    def test_getitem_invalid_type(self, filled_collection):
        with pytest.raises(TypeError):
            _ = filled_collection["неверный"]

    def test_getitem_float_index(self, filled_collection):
        with pytest.raises(TypeError):
            _ = filled_collection[1.5]


class TestBookCollectionAddition:
    def test_add_two_collections(self, sample_books):
        col1 = BookCollection(sample_books[:2])
        col2 = BookCollection(sample_books[2:])
        result = col1 + col2
        assert isinstance(result, BookCollection)
        assert len(result) == 4

    def test_add_collection_with_list(self, sample_books):
        col = BookCollection(sample_books[:2])
        result = col + sample_books[2:]
        assert isinstance(result, BookCollection)
        assert len(result) == 4

    def test_add_empty_collections(self):
        col1 = BookCollection()
        col2 = BookCollection()
        result = col1 + col2
        assert len(result) == 0

    def test_add_invalid_type(self, filled_collection):
        with pytest.raises(TypeError):
            _ = filled_collection + "неверно"

    def test_add_with_dict(self, filled_collection):
        with pytest.raises(TypeError):
            _ = filled_collection + {"ключ": "значение"}


class TestBookCollectionMethods:
    def test_add_book(self, empty_collection, sample_books):
        empty_collection.add(sample_books[0])
        assert len(empty_collection) == 1
        assert sample_books[0] in empty_collection

    def test_add_multiple_books(self, empty_collection, sample_books):
        for book in sample_books:
            empty_collection.add(book)
        assert len(empty_collection) == 4

    def test_remove_book(self, filled_collection, sample_books):
        filled_collection.remove(sample_books[0])
        assert len(filled_collection) == 3
        assert sample_books[0] not in filled_collection

    def test_remove_nonexistent_book(self, filled_collection):
        nonexistent = Book("Несуществующая", "Неизвестный", 2000, "Фантастика", "999")
        filled_collection.remove(nonexistent)
        assert len(filled_collection) == 4


class TestBookCollectionContains:
    def test_contains_existing_book(self, filled_collection, sample_books):
        assert sample_books[0] in filled_collection
        assert sample_books[1] in filled_collection

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

    def test_creation_with_mixed_types(self, sample_books):
        with pytest.raises(TypeError) as exc_info:
            IndexDict(sample_books + [None])
        assert "Ожидался объект Book" in str(exc_info.value)


class TestIndexDictGetItem:
    def test_getitem_by_isbn(self, sample_books):
        index = IndexDict(sample_books)
        book = index['isbn', '978-1']
        assert book == sample_books[0]

    def test_getitem_by_author(self, sample_books):
        index = IndexDict(sample_books)
        results = index['author', 'Лев Толстой']
        assert isinstance(results, BookCollection)
        assert len(results) == 2

    def test_getitem_by_year(self, sample_books):
        index = IndexDict(sample_books)
        results = index['year', 1869]
        assert isinstance(results, BookCollection)
        assert len(results) == 2

    def test_getitem_nonexistent_isbn(self, sample_books):
        index = IndexDict(sample_books)
        result = index['isbn', '999-999']
        assert result is None

    def test_getitem_nonexistent_author(self, sample_books):
        index = IndexDict(sample_books)
        results = index['author', 'Неизвестный Автор']
        assert isinstance(results, BookCollection)
        assert len(results) == 0

    def test_getitem_invalid_index_type(self, sample_books):
        index = IndexDict(sample_books)
        with pytest.raises(KeyError):
            _ = index['неверный_тип', 'значение']

    def test_getitem_not_tuple(self, sample_books):
        index = IndexDict(sample_books)
        with pytest.raises(TypeError):
            _ = index['isbn']

    def test_getitem_wrong_tuple_length(self, sample_books):
        index = IndexDict(sample_books)
        with pytest.raises(TypeError):
            _ = index['isbn', 'значение', 'лишнее']


class TestIndexDictMethods:
    def test_add_book(self, sample_books):
        index = IndexDict()
        index.add_book(sample_books[0])
        assert len(index) == 1
        assert index['isbn', '978-1'] == sample_books[0]

    def test_add_multiple_books_same_author(self, sample_books):
        index = IndexDict()
        index.add_book(sample_books[0])
        index.add_book(sample_books[1])
        results = index['author', 'Лев Толстой']
        assert len(results) == 2

    def test_add_book_with_invalid_type_none(self):
        index = IndexDict()
        with pytest.raises(TypeError) as exc_info:
            index.add_book(None)
        assert "Ожидался объект Book" in str(exc_info.value)

    def test_add_book_with_invalid_type_string(self):
        index = IndexDict()
        with pytest.raises(TypeError) as exc_info:
            index.add_book("не книга")
        assert "Ожидался объект Book" in str(exc_info.value)

    def test_add_book_with_invalid_type_dict(self):
        index = IndexDict()
        with pytest.raises(TypeError) as exc_info:
            index.add_book({"title": "Книга"})
        assert "Ожидался объект Book" in str(exc_info.value)

    def test_remove_book(self, sample_books):
        index = IndexDict(sample_books)
        index.remove_book(sample_books[0])
        assert len(index) == 3
        assert index['isbn', '978-1'] is None

    def test_remove_book_cleans_empty_indices(self, sample_books):
        index = IndexDict([sample_books[2]])
        index.remove_book(sample_books[2])
        results = index['author', 'Михаил Булгаков']
        assert len(results) == 0

    def test_remove_nonexistent_book(self, sample_books):
        index = IndexDict(sample_books)
        nonexistent = Book("Несуществующая", "Неизвестный", 2000, "Фантастика", "999")
        index.remove_book(nonexistent)
        assert len(index) == 4


class TestIndexDictContains:
    def test_contains_book_object(self, sample_books):
        index = IndexDict(sample_books)
        assert sample_books[0] in index
        assert sample_books[1] in index

    def test_contains_isbn_string(self, sample_books):
        index = IndexDict(sample_books)
        assert '978-1' in index
        assert '978-2' in index

    def test_not_contains_book(self, sample_books):
        index = IndexDict(sample_books)
        nonexistent = Book("Несуществующая", "Неизвестный", 2000, "Фантастика", "999")
        assert nonexistent not in index
        assert '999' not in index

    def test_contains_invalid_type(self, sample_books):
        index = IndexDict(sample_books)
        assert 123 not in index
        assert [sample_books[0]] not in index


class TestBookCollectionStr:
    def test_str_empty_collection(self):
        collection = BookCollection()
        assert str(collection) == "Количество книг: 0"

    def test_str_filled_collection(self, sample_books):
        collection = BookCollection(sample_books)
        assert str(collection) == "Количество книг: 4"

    def test_str_single_book(self, sample_books):
        collection = BookCollection([sample_books[0]])
        assert str(collection) == "Количество книг: 1"


class TestIndexDictStr:
    def test_str_empty_index(self):
        index = IndexDict()
        assert str(index) == "Количество уникальных книг: 0"

    def test_str_filled_index(self, sample_books):
        index = IndexDict(sample_books)
        assert str(index) == "Количество уникальных книг: 4"

    def test_str_single_book(self, sample_books):
        index = IndexDict([sample_books[0]])
        assert str(index) == "Количество уникальных книг: 1"


class TestBookCollectionEquality:
    def test_equality_same_books_same_order(self, sample_books):
        col1 = BookCollection(sample_books[:3])
        col2 = BookCollection(sample_books[:3])
        assert col1 == col2

    def test_equality_different_books(self, sample_books):
        col1 = BookCollection(sample_books[:2])
        col2 = BookCollection(sample_books[2:4])
        assert col1 != col2

    def test_equality_different_order(self, sample_books):
        col1 = BookCollection([sample_books[0], sample_books[1]])
        col2 = BookCollection([sample_books[1], sample_books[0]])
        assert col1 != col2

    def test_equality_empty_collections(self):
        col1 = BookCollection()
        col2 = BookCollection()
        assert col1 == col2

    def test_equality_with_non_collection(self, sample_books):
        col = BookCollection(sample_books)
        assert col != sample_books
        assert col != "строка"
        assert col != 123


class TestIndexDictEquality:
    def test_equality_same_books(self, sample_books):
        index1 = IndexDict(sample_books)
        index2 = IndexDict(sample_books)
        assert index1 == index2

    def test_equality_different_books(self, sample_books):
        index1 = IndexDict(sample_books[:2])
        index2 = IndexDict(sample_books[2:])
        assert index1 != index2
    def test_equality_empty_indexes(self):
        index1 = IndexDict()
        index2 = IndexDict()
        assert index1 == index2

    def test_equality_with_non_index(self, sample_books):
        index = IndexDict(sample_books)
        assert index != sample_books
        assert index != "строка"
        assert index != 123


class TestBookCollectionRepr:
    def test_repr_contains_class_name(self, sample_books):
        col = BookCollection(sample_books[:2])
        result = repr(col)
        assert "BookCollection" in result

    def test_repr_empty_collection(self):
        col = BookCollection()
        result = repr(col)
        assert "BookCollection" in result
        assert "[]" in result


class TestIndexDictRepr:
    def test_repr_contains_class_name(self, sample_books):
        index = IndexDict(sample_books)
        result = repr(index)
        assert "IndexDict" in result

    def test_repr_shows_counts(self, sample_books):
        index = IndexDict(sample_books)
        result = repr(index)
        assert "isbn_count=" in result
        assert "authors=" in result
        assert "years=" in result
