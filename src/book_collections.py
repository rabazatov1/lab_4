from abc import ABC, abstractmethod
from src.book import Book


class BaseCollection(ABC):
    """Базовый абстрактный класс для коллекций книг."""

    @abstractmethod
    def __iter__(self):
        """
        Итерация по элементам коллекции

        :return: Итератор по элементам коллекции.
        :rtype: Iterator
        """
        pass

    @abstractmethod
    def __len__(self):
        """
        Возвращает размер коллекции

        :return: Количество элементов в коллекции.
        :rtype: int
        """
        pass

    @abstractmethod
    def __getitem__(self, key):
        """
        Доступ к элементам коллекции по ключу или индексу

        :param key: Ключ или индекс для доступа к элементу
        :return: Элемент коллекции
        """
        pass

    @abstractmethod
    def __str__(self):
        """
        Строковое представление коллекции

        :return: Строковое представление коллекции
        :rtype: str
        """
        pass

    def __contains__(self, item):
        """
        Проверка наличия элемента в коллекции

        :param item: Элемент для проверки
        :return: True если элемент найден, False иначе
        :rtype: bool
        """
        for element in self:
            if element == item:
                return True
        return False


class BookCollection(BaseCollection):
    """Пользовательская списковая коллекция книг с поддержкой индексов и срезов."""

    def __init__(self, data=None):
        """
        Инициализация коллекции книг

        :param data: Итерируемый объект с книгами для инициализации (необязательно)
        :type data: iterable, optional
        :raises TypeError: Если data не является итерируемым объектом
        """
        if data is None:
            self._books = []
        else:
            try:
                self._books = list(data)
            except TypeError:
                raise TypeError("data должен быть итерируемым объектом")

    def __iter__(self):
        """
        Возвращает итератор по книгам в коллекции

        :return: Итератор по списку книг
        :rtype: Iterator
        """
        return iter(self._books)

    def __len__(self):
        """
        Возвращает количество книг в коллекции

        :return: Количество книг
        :rtype: int
        """
        return len(self._books)

    def __getitem__(self, index):
        """
        Доступ к книгам по индексу или срезу

        :param index: Целочисленный индекс или срез
        :type index: int or slice
        :return: Книга при индексе, новая коллекция при срезе
        :rtype: Book or BookCollection
        :raises TypeError: Если индекс не является int или slice
        """
        if isinstance(index, slice):
            return BookCollection(self._books[index])
        if isinstance(index, int):
            return self._books[index]
        raise TypeError("Индекс должен быть int или slice")

    def __add__(self, other):
        """
        Сложение коллекций книг

        :param other: BookCollection или list для объединения
        :type other: BookCollection or list
        :return: Новая коллекция с объединенными книгами
        :rtype: BookCollection
        :raises TypeError: Если other не является BookCollection или list
        """
        if isinstance(other, BookCollection):
            other_data = other._books
        elif isinstance(other, list):
            other_data = other
        else:
            raise TypeError("Можно складывать только с BookCollection или list")
        return BookCollection(self._books + list(other_data))

    def add(self, book: Book):
        """
        Добавляет книгу в конец коллекции

        :param book: Книга для добавления
        :type book: Book
        """
        self._books.append(book)

    def remove(self, book: Book):
        """
        Удаляет книгу из коллекции

        :param book: Книга для удаления
        :type book: Book
        """
        if book in self._books:
            self._books.remove(book)

    def __contains__(self, item: Book):
        """
        Проверяет наличие книги в коллекции

        :param item: Книга для проверки
        :type item: Book
        :return: True если книга найдена, False иначе
        :rtype: bool
        """
        return item in self._books

    def __str__(self) -> str:
        """
        Строковое представление коллекции

        :return: Строка с информацией о количестве книг
        :rtype: str
        """
        return f"Количество книг: {len(self._books)}"

    def __eq__(self, other) -> bool:
        """
        Сравнение коллекций по содержимому

        :param other: Объект для сравнения
        :type other: BookCollection or any
        :return: True если коллекции содержат одинаковые книги в том же порядке
        :rtype: bool
        """
        if not isinstance(other, BookCollection):
            return False
        return self._books == other._books

    def __repr__(self) -> str:
        """
        Представление коллекции для отладки

        :return: Строка с информацией о коллекции
        :rtype: str
        """
        return f"BookCollection({self._books!r})"


class IndexDict(BaseCollection):
    """Пользовательская словарная коллекция для индексации книг по ISBN, автору и году."""

    def __init__(self, books=None):
        """
        Инициализация индексной коллекции

        :param books: Итерируемый объект с книгами для построения индексов (необязательно)
        :type books: iterable, optional
        """
        self._index_by_isbn = {}
        self._index_by_author = {}
        self._index_by_year = {}

        if books is not None:
            self._build_indexes(books)

    def _build_indexes(self, books) -> None:
        """
        Построение всех индексов из коллекции книг

        :param books: Итерируемый объект с книгами
        :type books: iterable
        :raises TypeError: Если объект в books не является Book
        """
        for book in books:
            if not isinstance(book, Book):
                raise TypeError(f"Ожидался объект Book, получен {type(book).__name__}")
            self._index_by_isbn[book.isbn] = book
            if book.author not in self._index_by_author:
                self._index_by_author[book.author] = []
            self._index_by_author[book.author].append(book)
            if book.year not in self._index_by_year:
                self._index_by_year[book.year] = []
            self._index_by_year[book.year].append(book)

    def __getitem__(self, key):
        """
        Доступ к индексам по кортежу (тип индекса, значение)

        :param key: Кортеж вида ('isbn', значение), ('author', значение) или ('year', значение)
        :type key: tuple
        :return: Книга для ISBN, коллекция для author/year
        :rtype: Book or BookCollection
        :raises TypeError: Если ключ не является кортежем из двух элементов
        :raises KeyError: Если тип индекса неизвестен.
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
        """
        Итерация по всем уникальным книгам

        :return: Итератор по книгам из индекса ISBN
        :rtype: Iterator
        """
        return iter(self._index_by_isbn.values())

    def __len__(self) -> int:
        """
        Возвращает количество уникальных книг

        :return: Количество уникальных книг по ISBN
        :rtype: int
        """
        return len(self._index_by_isbn)

    def add_book(self, book: Book) -> None:
        """
        Добавляет книгу во все индексы

        :param book: Книга для добавления
        :type book: Book
        :raises TypeError: Если book не является объектом Book
        """
        if not isinstance(book, Book):
            raise TypeError(f"Ожидался объект Book, получен {type(book).__name__}")
        self._index_by_isbn[book.isbn] = book
        if book.author not in self._index_by_author:
            self._index_by_author[book.author] = []
        self._index_by_author[book.author].append(book)
        if book.year not in self._index_by_year:
            self._index_by_year[book.year] = []
        self._index_by_year[book.year].append(book)

    def remove_book(self, book: Book) -> None:
        """
        Удаляет книгу из всех индексов

        :param book: Книга для удаления
        :type book: Book
        """
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

    def __contains__(self, item) -> bool:
        """
        Проверяет наличие книги в индексе по ISBN

        :param item: Книга (Book) или ISBN (str) для проверки
        :type item: Book or str
        :return: True если книга найдена, False иначе
        :rtype: bool
        """
        if isinstance(item, Book):
            return item.isbn in self._index_by_isbn
        elif isinstance(item, str):
            return item in self._index_by_isbn
        return False

    def __str__(self) -> str:
        """
        Строковое представление индексной коллекции

        :return: Строка с информацией о количестве уникальных книг
        :rtype: str
        """
        return f"Количество уникальных книг: {len(self)}"

    def __eq__(self, other) -> bool:
        """
        Сравнение индексных коллекций по содержимому

        :param other: Объект для сравнения
        :type other: IndexDict or any
        :return: True если индексы содержат одинаковые книги
        :rtype: bool
        """
        if not isinstance(other, IndexDict):
            return False
        return self._index_by_isbn == other._index_by_isbn

    def __repr__(self) -> str:
        """
        Представление индексной коллекции для отладки

        :return: Строка с информацией об индексах
        :rtype: str
        """
        return (f"IndexDict(isbn_count={len(self._index_by_isbn)}, "
                f"authors={len(self._index_by_author)}, "
                f"years={len(self._index_by_year)})")
