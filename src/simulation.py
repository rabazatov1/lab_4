"""Модуль с функцией симуляции работы библиотеки."""

import random
from src.library import Library
from src.constants import create_sample_books, GENRES, AUTHORS, YEARS, FAKE_ISBNS


def run_simulation(steps: int = 20, seed: int | None = None) -> None:
    """
    Выполняет псевдослучайную симуляцию работы библиотеки

    :param steps: Количество шагов симуляции
    :type steps: int
    :param seed: Seed для генератора случайных чисел
    :type seed: int or None
    """
    if seed is not None:
        random.seed(seed)

    print("ПСЕВДОСЛУЧАЙНАЯ СИМУЛЯЦИЯ")
    print(f"Параметры: steps={steps}, seed={seed}")
    print()

    library = Library()
    available_books = create_sample_books()

    print("Инициализация библиотеки")
    for book in available_books[:10]:
        library.add_book(book)
        print(f"Добавлена книга: {book}")
    print(f"\nНачальное состояние: {library}")
    print()

    events = [
        "add_book",
        "remove_book",
        "search_by_author",
        "search_by_genre",
        "search_by_year",
        "search_nonexistent",
    ]

    for step in range(1, steps + 1):
        print(f"Шаг {step}")

        event = random.choice(events)

        try:
            match event:
                case "add_book":
                    _event_add_book(library, available_books)
                case "remove_book":
                    _event_remove_book(library)
                case "search_by_author":
                    _event_search_by_author(library)
                case "search_by_genre":
                    _event_search_by_genre(library)
                case "search_by_year":
                    _event_search_by_year(library)
                case "search_nonexistent":
                    _event_search_nonexistent(library)
                case _:
                    print(f"Неизвестное событие: {event}")

        except Exception as e:
            print(f"Ошибка: {e}")
        print()

    print("ФИНАЛЬНОЕ СОСТОЯНИЕ")
    print(f"Всего книг: {len(library.books)}")
    print(f"Уникальных книг в индексе: {len(library.indexes)}")
    print()


def _event_add_book(library: Library, available_books: list):
    """
    Событие симуляции: добавление новой книги в библиотеку

    :param library: Объект библиотеки
    :type library: Library
    :param available_books: Список доступных книг для добавления
    :type available_books: list
    """
    available = [book for book in available_books if book.isbn not in library.indexes]

    if not available:
        print("Событие: Добавление книги")
        print("Все доступные книги уже в библиотеке")
        return

    book = random.choice(available)
    try:
        library.add_book(book)
        print("Событие: Добавление книги")
        print(f"Добавлена: {book}")
        print(f"Текущее количество книг: {len(library.books)}")
    except ValueError as e:
        print("Событие: Добавление книги")
        print(f"Не удалось добавить книгу: {e}")


def _event_remove_book(library: Library):
    """
    Событие симуляции: удаление случайной книги из библиотеки

    :param library: Объект библиотеки
    :type library: Library
    """
    print("Событие: Удаление книги")

    if len(library.books) == 0:
        print("Библиотека пуста, нечего удалять")
        return

    book = library.get_random_book()
    if book:
        library.remove_book(book)
        print(f"Удалена: {book}")
        print(f"Текущее количество книг: {len(library.books)}")


def _event_search_by_author(library: Library):
    """
    Событие симуляции: поиск книг по случайному автору

    :param library: Объект библиотеки
    :type library: Library
    """
    author = random.choice(AUTHORS)
    print(f"Событие: Поиск по автору '{author}'")

    results = library.search_by_author(author)
    print(f"Найдено книг: {len(results)}")

    if len(results) > 0:
        for book in results:
            print(f"     - {book}")


def _event_search_by_genre(library: Library):
    """
    Событие симуляции: поиск книг по случайному жанру

    :param library: Объект библиотеки
    :type library: Library
    """
    genre = random.choice(GENRES)
    print(f"Событие: Поиск по жанру '{genre}'")

    results = library.search_by_genre(genre)
    print(f"Найдено книг: {len(results)}")

    if len(results) > 0:
        for book in results:
            print(f"     - {book}")


def _event_search_by_year(library: Library):
    """
    Событие симуляции: поиск книг по случайному году издания

    :param library: Объект библиотеки
    :type library: Library
    """
    year = random.choice(YEARS)
    print(f"Событие: Поиск по году {year}")

    results = library.search_by_year(year)
    print(f"Найдено книг: {len(results)}")

    if len(results) > 0:
        for book in results:
            print(f"     - {book}")


def _event_search_nonexistent(library: Library):
    """
    Событие симуляции: поиск несуществующей книги для проверки обработки

    :param library: Объект библиотеки
    :type library: Library
    """
    isbn = random.choice(FAKE_ISBNS)
    print(f"Событие: Поиск несуществующей книги (ISBN: {isbn})")

    result = library.search_by_isbn(isbn)
    if result is None:
        print("Книга не найдена (ожидаемое поведение)")
    else:
        print(f"Неожиданно найдена книга: {result}")
