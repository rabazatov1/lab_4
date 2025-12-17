class Book:
    def __init__(self, title, author, year, genre, isbn):
        self.title = title
        self.author = author
        self.year = year
        self.genre = genre
        self.isbn = isbn

    def __str__(self) -> str:
        """Строковое представление книги для пользователя."""
        return f"{self.title} - {self.author} ({self.year})"

    def __eq__(self, other) -> bool:
        """Сравнение книг по ISBN."""
        if isinstance(other, Book):
            return self.isbn == other.isbn
        return False
