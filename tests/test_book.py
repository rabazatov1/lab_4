from src.book import Book


class TestBookCreation:
    def test_book_creation_normal(self):
        book = Book("Война и мир", "Лев Толстой", 1869, "Роман", "978-5-17-123456-7")
        assert book.title == "Война и мир"
        assert book.author == "Лев Толстой"
        assert book.year == 1869
        assert book.genre == "Роман"
        assert book.isbn == "978-5-17-123456-7"

    def test_book_creation_edge_case_empty_strings(self):
        book = Book("", "", 0, "", "")
        assert book.title == ""
        assert book.year == 0


class TestBookStr:
    def test_str_normal(self):
        book = Book("Мастер и Маргарита", "Михаил Булгаков", 1967, "Роман", "978-5-17-098765-4")
        assert str(book) == "Мастер и Маргарита - Михаил Булгаков (1967)"


class TestBookEquality:
    def test_equality_same_isbn(self):
        book1 = Book("Евгений Онегин", "Александр Пушкин", 1833, "Поэма", "978-5-17-111111-1")
        book2 = Book("Евгений Онегин (другое издание)", "А.С. Пушкин", 1833, "Поэзия", "978-5-17-111111-1")
        assert book1 == book2

    def test_equality_different_isbn(self):
        book1 = Book("Идиот", "Фёдор Достоевский", 1869, "Роман", "978-5-17-222222-2")
        book2 = Book("Идиот", "Фёдор Достоевский", 1869, "Роман", "978-5-17-333333-3")
        assert book1 != book2

    def test_equality_with_none(self):
        book = Book("Доктор Живаго", "Борис Пастернак", 1957, "Роман", "978-5-17-555555-5")
        assert book is not None


class TestBookRepr:
    def test_repr_normal(self):
        book = Book("Война и мир", "Лев Толстой", 1869, "Роман", "978-1")
        result = repr(book)
        assert "Book(" in result
        assert "title='Война и мир'" in result
        assert repr(book) != str(book)
