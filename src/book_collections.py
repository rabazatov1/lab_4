from abc import ABC, abstractmethod
from src.book import Book


class BaseCollection(ABC):
    """
    Базовый абстрактный класс для коллекций книг.
    Определяет общий интерфейс для всех коллекций.
    """

    @abstractmethod
    def __iter__(self):
        """Итерация по элементам коллекции."""
        pass

    @abstractmethod
    def __len__(self):
        """Размер коллекции."""
        pass

    @abstractmethod
    def __getitem__(self, key):
        """Доступ к элементам коллекции."""
        pass

    @abstractmethod
    def __str__(self):
        """
        Строковое представление коллекции.
        Базовая реализация - может быть переопределена.
        """
        pass

    def __contains__(self, item):
        """
        Проверка наличия элемента в коллекции.
        Базовая реализация - может быть переопределена.
        """
        for element in self:
            if element == item:
                return True
        return False


class BookCollection(BaseCollection):
    """Пользовательская списковая коллекция книг."""

    def __init__(self, data=None):
        self._books = list(data) if data is not None else []

    def __iter__(self):
        return iter(self._books)

    def __len__(self):
        return len(self._books)

    def __getitem__(self, index):
        if isinstance(index, slice):
            return BookCollection(self._books[index])
        if isinstance(index, int):
            return self._books[index]
        raise TypeError("Индекс должен быть int или slice")

    def __add__(self, other):
        if isinstance(other, BookCollection):
            other_data = other._books
        elif isinstance(other, list):
            other_data = other
        else:
            raise TypeError("Можно складывать только с BookCollection или list")
        return BookCollection(self._books + list(other_data))

    def add(self, book: Book):
        """Добавить книгу в коллекцию."""
        self._books.append(book)

    def remove(self, book: Book):
        """Удалить книгу из коллекции."""
        if book in self._books:
            self._books.remove(book)

    def __contains__(self, item: Book):
        """Проверка наличия книги в коллекции."""
        return item in self._books

    def __str__(self) -> str:
        """Строковое представление коллекции."""
        return f"BookCollection({len(self._books)} books)"


class IndexDict(BaseCollection):
    """
    Пользовательская словарная коллекция для индексации книг.
    Индексирует книги по ISBN, Author, Year.
    """

    def __init__(self, books=None):
        self._index_by_isbn = {}
        self._index_by_author = {}
        self._index_by_year = {}

        if books is not None:
            self._build_indexes(books)

    def _build_indexes(self, books) -> None:
        """Построить индексы из коллекции книг."""
        for book in books:
            self._index_by_isbn[book.isbn] = book
            if book.author not in self._index_by_author:
                self._index_by_author[book.author] = []
            self._index_by_author[book.author].append(book)
            if book.year not in self._index_by_year:
                self._index_by_year[book.year] = []
            self._index_by_year[book.year].append(book)

    def __getitem__(self, key):
        """
        Доступ к индексам:
        - index_dict['isbn', '123'] -> книга по ISBN
        - index_dict['author', 'Tolstoy'] -> список книг автора
        - index_dict['year', 2020] -> список книг года
        """
        if isinstance(key, tuple) and len(key) == 2:
            index_type, value = key
            if index_type == 'isbn':
                return self._index_by_isbn.get(value)
            elif index_type == 'author':
                return BookCollection(self._index_by_author.get(value, []))
            elif index_type == 'year':
                return BookCollection(self._index_by_year.get(value, []))
            else:
                raise KeyError(f"Неизвестный тип индекса: {index_type}")
        raise TypeError("Ключ должен быть кортежем (тип, значение)")

    def __iter__(self):
        """Итерация по всем уникальным книгам (по ISBN)."""
        return iter(self._index_by_isbn.values())

    def __len__(self) -> int:
        """Количество уникальных книг (по ISBN)."""
        return len(self._index_by_isbn)

    def add_book(self, book: Book) -> None:
        """Добавить книгу в индексы."""
        self._index_by_isbn[book.isbn] = book
        if book.author not in self._index_by_author:
            self._index_by_author[book.author] = []
        self._index_by_author[book.author].append(book)
        if book.year not in self._index_by_year:
            self._index_by_year[book.year] = []
        self._index_by_year[book.year].append(book)

    def remove_book(self, book: Book) -> None:
        """Удалить книгу из индексов."""
        if book.isbn in self._index_by_isbn:
            del self._index_by_isbn[book.isbn]
        if book.author in self._index_by_author:
            if book in self._index_by_author[book.author]:
                self._index_by_author[book.author].remove(book)
            if not self._index_by_author[book.author]:
                del self._index_by_author[book.author]
        if book.year in self._index_by_year:
            if book in self._index_by_year[book.year]:
                self._index_by_year[book.year].remove(book)
            if not self._index_by_year[book.year]:
                del self._index_by_year[book.year]

    def update_from_collection(self, books) -> None:
        """Обновить индексы на основе коллекции книг."""
        self._index_by_isbn.clear()
        self._index_by_author.clear()
        self._index_by_year.clear()
        self._build_indexes(books)

    def __contains__(self, item) -> bool:
        """
        Магический метод для проверки наличия книги по ISBN.
        Отражает предметную область - проверка наличия книги в библиотеке.
        """
        if isinstance(item, Book):
            return item.isbn in self._index_by_isbn
        elif isinstance(item, str):
            return item in self._index_by_isbn
        return False

    def __str__(self) -> str:
        """Строковое представление индексной коллекции."""
        return f"IndexDict({len(self)} unique books)"
