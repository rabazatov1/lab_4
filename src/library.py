from src.book import Book
from src.book_collections import BookCollection, IndexDict


class Library:
    """
    Класс библиотеки, содержащий коллекцию книг и индексы.
    Методы поиска используют кастомные коллекции.
    """

    def __init__(self, books=None):
        self.books = books if books is not None else BookCollection()
        self.indexes = IndexDict(self.books)

    def add_book(self, book: Book):
        """Добавить книгу в библиотеку"""
        self.books.add(book)
        self.indexes.add_book(book)

    def remove_book(self, book: Book):
        """Удалить книгу из библиотеки"""
        self.books.remove(book)
        self.indexes.remove_book(book)

    def search_by_isbn(self, isbn: str):
        """Поиск книги по ISBN"""
        return self.indexes['isbn', isbn]

    def search_by_author(self, author: str):
        """Поиск книг по автору"""
        result = self.indexes['author', author]
        return result if result is not None else BookCollection()

    def search_by_year(self, year: int):
        """Поиск книг по году"""
        result = self.indexes['year', year]
        return result if result is not None else BookCollection()

    def search_by_genre(self, genre: str) :
        """Поиск книг по жанру (использует BookCollection напрямую)"""
        result = BookCollection()
        for book in self.books:
            if book.genre == genre:
                result.add(book)
        return result

    def update_indexes(self):
        """Обновить индексы на основе текущей коллекции книг"""
        self.indexes.update_from_collection(self.books)

    def __str__(self):
        return f"Library({len(self.books)} books, {len(self.indexes)} indexed)"
