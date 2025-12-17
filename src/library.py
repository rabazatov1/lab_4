import random
from src.book import Book
from src.book_collections import BookCollection, IndexDict


class Library:
    """Класс библиотеки, содержащий коллекцию книг и индексы для быстрого поиска."""

    def __init__(self, books=None):
        """
        Инициализация библиотеки

        :param books: Начальная коллекция книг или None
        :type books: BookCollection, optional
        """
        self.books = books if books is not None else BookCollection()
        self.indexes = IndexDict(self.books)

    def add_book(self, book: Book):
        """
        Добавляет книгу в библиотеку и обновляет индексы

        :param book: Книга для добавления
        :type book: Book
        :raises ValueError: Если книга с таким ISBN уже существует
        """
        if book.isbn in self.indexes:
            raise ValueError(f"Книга с ISBN '{book.isbn}' уже существует в библиотеке")
        self.books.add(book)
        self.indexes.add_book(book)

    def remove_book(self, book: Book):
        """
        Удаляет книгу из библиотеки и обновляет индексы

        :param book: Книга для удаления
        :type book: Book
        """
        self.books.remove(book)
        self.indexes.remove_book(book)

    def search_by_isbn(self, isbn: str):
        """
        Поиск книги по уникальному идентификатору ISBN

        :param isbn: ISBN для поиска
        :type isbn: str
        :return: Найденная книга или None
        :rtype: Book or None
        """
        return self.indexes['isbn', isbn]

    def search_by_author(self, author: str):
        """
        Поиск всех книг указанного автора

        :param author: Имя автора для поиска
        :type author: str
        :return: Коллекция книг автора
        :rtype: BookCollection
        """
        result = self.indexes['author', author]
        return result if result is not None else BookCollection()

    def search_by_year(self, year: int):
        """
        Поиск всех книг изданных в указанном году

        :param year: Год издания для поиска
        :type year: int
        :return: Коллекция книг данного года
        :rtype: BookCollection
        """
        result = self.indexes['year', year]
        return result if result is not None else BookCollection()

    def search_by_genre(self, genre: str):
        """
        Поиск всех книг указанного жанра

        :param genre: Жанр для поиска
        :type genre: str
        :return: Коллекция книг данного жанра
        :rtype: BookCollection
        """
        result = BookCollection()
        for book in self.books:
            if book.genre == genre:
                result.add(book)
        return result

    def get_random_book(self):
        """
        Получает случайную книгу из библиотеки

        :return: Случайная книга или None если библиотека пуста
        :rtype: Book or None
        """
        if len(self.books) == 0:
            return None
        books_list = self.books._books
        return random.choice(books_list)

    def __str__(self):
        """
        Строковое представление библиотеки

        :return: Строка с информацией о количестве книг
        :rtype: str
        """
        return (f"Общее количество книг: {len(self.books)},"
                f" количество уникальных книг: {len(self.indexes)}")
