import pytest
from src.book import Book


class TestBookCreation:
    def test_book_creation_normal(self):
        book = Book("Война и мир", "Лев Толстой", 1869, "Роман", "978-5-17-123456-7")
        assert book.title == "Война и мир"
        assert book.author == "Лев Толстой"
        assert book.year == 1869
        assert book.genre == "Роман"
        assert book.isbn == "978-5-17-123456-7"

    def test_book_creation_with_unicode(self):
        book = Book("Преступление и наказание", "Фёдор Достоевский", 1866, "Роман", "978-5-389-01234-5")
        assert book.title == "Преступление и наказание"
        assert book.author == "Фёдор Достоевский"

    def test_book_creation_edge_case_empty_strings(self):
        book = Book("", "", 0, "", "")
        assert book.title == ""
        assert book.author == ""
        assert book.year == 0
        assert book.genre == ""
        assert book.isbn == ""

    def test_book_creation_edge_case_very_old_year(self):
        book = Book("Библия", "Разные авторы", -1000, "Религия", "Н/Д")
        assert book.year == -1000

    def test_book_creation_edge_case_future_year(self):
        book = Book("Книга будущего", "Неизвестно", 3000, "Фантастика", "999-9-99-999999-9")
        assert book.year == 3000


class TestBookStr:
    def test_str_normal(self):
        book = Book("Мастер и Маргарита", "Михаил Булгаков", 1967, "Роман", "978-5-17-098765-4")
        assert str(book) == "Мастер и Маргарита - Михаил Булгаков (1967)"

    def test_str_with_unicode(self):
        book = Book("Анна Каренина", "Лев Толстой", 1877, "Роман", "978-5-389-12345-6")
        assert str(book) == "Анна Каренина - Лев Толстой (1877)"

    def test_str_edge_case_empty(self):
        book = Book("", "", 0, "", "")
        assert str(book) == " -  (0)"


class TestBookEquality:
    def test_equality_same_isbn(self):
        book1 = Book("Евгений Онегин", "Александр Пушкин", 1833, "Поэма", "978-5-17-111111-1")
        book2 = Book("Евгений Онегин (другое издание)", "А.С. Пушкин", 1833, "Поэзия", "978-5-17-111111-1")
        assert book1 == book2

    def test_equality_different_isbn(self):
        book1 = Book("Идиот", "Фёдор Достоевский", 1869, "Роман", "978-5-17-222222-2")
        book2 = Book("Идиот", "Фёдор Достоевский", 1869, "Роман", "978-5-17-333333-3")
        assert book1 != book2

    def test_equality_same_object(self):
        book = Book("Тихий Дон", "Михаил Шолохов", 1940, "Роман", "978-5-17-444444-4")
        assert book == book

    def test_equality_with_none(self):
        book = Book("Доктор Живаго", "Борис Пастернак", 1957, "Роман", "978-5-17-555555-5")
        assert book != None

    def test_equality_with_string(self):
        book = Book("Капитанская дочка", "Александр Пушкин", 1836, "Повесть", "978-5-17-666666-6")
        assert book != "978-5-17-666666-6"

    def test_equality_with_number(self):
        book = Book("Мёртвые души", "Николай Гоголь", 1842, "Поэма", "978-5-17-777777-7")
        assert book != 1842

    def test_equality_with_dict(self):
        book = Book("Отцы и дети", "Иван Тургенев", 1862, "Роман", "978-5-17-888888-8")
        assert book != {"isbn": "978-5-17-888888-8"}

    def test_equality_empty_isbn(self):
        book1 = Book("Книга1", "Автор1", 2020, "Жанр1", "")
        book2 = Book("Книга2", "Автор2", 2021, "Жанр2", "")
        assert book1 == book2


class TestBookRepr:
    def test_repr_normal(self):
        book = Book("Война и мир", "Лев Толстой", 1869, "Роман", "978-1")
        result = repr(book)
        assert "Book(" in result
        assert "title='Война и мир'" in result
        assert "author='Лев Толстой'" in result
        assert "year=1869" in result
        assert "genre='Роман'" in result
        assert "isbn='978-1'" in result

    def test_repr_different_from_str(self):
        book = Book("Война и мир", "Лев Толстой", 1869, "Роман", "978-1")
        assert repr(book) != str(book)
    def test_repr_with_quotes(self):
        book = Book("Книга с 'кавычками'", "Автор", 2020, "Жанр", "ISBN-1")
        result = repr(book)
        assert "Книга с 'кавычками'" in result
