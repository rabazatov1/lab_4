class Book:
    """Класс, представляющий книгу в библиотеке."""

    def __init__(self, title, author, year, genre, isbn):
        """
        Инициализация книги

        :param title: Название книги
        :type title: str
        :param author: Автор книги
        :type author: str
        :param year: Год издания
        :type year: int
        :param genre: Жанр книги
        :type genre: str
        :param isbn: Уникальный идентификатор ISBN
        :type isbn: str
        """
        self.title = title
        self.author = author
        self.year = year
        self.genre = genre
        self.isbn = isbn

    def __str__(self) -> str:
        """
        Строковое представление книги для пользователя

        :return: Строка в формате "Название - Автор (Год)"
        :rtype: str
        """
        return f"{self.title} - {self.author} ({self.year})"

    def __eq__(self, other) -> bool:
        """
        Сравнение книг по ISBN

        :param other: Объект для сравнения
        :type other: Book or any
        :return: True если ISBN совпадают, False иначе
        :rtype: bool
        """
        if isinstance(other, Book):
            return self.isbn == other.isbn
        return False

    def __repr__(self) -> str:
        """
        Представление книги для отладки

        :return: Строка с полной информацией о книге
        :rtype: str
        """
        return (f"Book(title={self.title!r}, author={self.author!r}, "
                f"year={self.year}, genre={self.genre!r}, isbn={self.isbn!r})")
