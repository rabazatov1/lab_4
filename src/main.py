from src.book import Book
from src.library import Library
from src.simulation import run_simulation


def menu():
    print("\n" + "-" * 80)
    print("МЕНЮ:")
    print("  1. Добавить книгу")
    print("  2. Удалить книгу")
    print("  3. Показать все книги")
    print("  4. Поиск по ISBN")
    print("  5. Поиск по автору")
    print("  6. Поиск по году")
    print("  7. Поиск по жанру")
    print("  8. Запустить симуляцию")
    print("  0. Выход")
    print("-" * 80)


def run_simulation_menu():
    print("ЗАПУСК СИМУЛЯЦИИ")
    print("-" * 80)

    steps_str = input("Количество шагов (по умолчанию 20): ").strip()
    steps = 20
    if steps_str:
        try:
            steps = int(steps_str)
        except ValueError:
            print("Задано неверное значение, по умолчанию используется 20")
            steps = 20

    seed_str = input("Seed (Enter для случайного): ").strip()
    seed = None
    if seed_str:
        try:
            seed = int(seed_str)
        except ValueError:
            print("Задано неверное значение seed, используется случайное")
            seed = None

    print()
    print("-" * 80)

    run_simulation(steps=steps, seed=seed)

    print("-" * 80)
    print("СИМУЛЯЦИЯ ЗАВЕРШЕНА\n")


def print_book_details(book):
    print(f"  Название: {book.title}")
    print(f"  Автор:    {book.author}")
    print(f"  Год:      {book.year}")
    print(f"  Жанр:     {book.genre}")
    print(f"  ISBN:     {book.isbn}")


class CLI:
    def __init__(self):
        self.library = Library()

    def run(self):
        exit_requested = False
        while not exit_requested:
            menu()
            choice = input("\nВыберите действие: ").strip()
            print()
            if choice == "0":
                exit_requested = True
                self.exit_program()
            else:
                self.selection_processing(choice)

    def selection_processing(self, choice: str):
        actions = {
            "1": self.add_book,
            "2": self.remove_book,
            "3": self.show_all_books,
            "4": self.search_by_isbn,
            "5": self.search_by_author,
            "6": self.search_by_year,
            "7": self.search_by_genre,
            "8": run_simulation_menu,
            "0": self.exit_program
        }
        action = actions.get(choice)
        if action:
            action()
        else:
            print("Неверный выбор (выберите 0-9)")

    def add_book(self):
        print("ДОБАВЛЕНИЕ КНИГИ")
        print("-" * 80)

        title = ""
        while not title:
            title = input("Название: ").strip()
            if not title:
                print("Название не может быть пустым, попробуйте снова")

        author = ""
        while not author:
            author = input("Автор: ").strip()
            if not author:
                print("Автор не может быть пустым, попробуйте снова")

        year = None
        while year is None:
            year_str = input("Год издания: ").strip()
            if not year_str:
                print("Год не может быть пустым, попробуйте снова")
                continue
            try:
                year = int(year_str)
                if year < 0 or year > 2025:
                    print("Некорректный год, попробуйте снова")
                    year = None
            except ValueError:
                print("Год должен быть числом, попробуйте снова")

        genre = ""
        while not genre:
            genre = input("Жанр: ").strip()
            if not genre:
                print("Жанр не может быть пустым, попробуйте снова")

        isbn = ""
        while not isbn:
            isbn = input("ISBN: ").strip()
            if not isbn:
                print("ISBN не может быть пустым, попробуйте снова")

        if self.library.search_by_isbn(isbn):
            print(f"Книга с ISBN {isbn} уже существует")
            return

        book = Book(title, author, year, genre, isbn)
        self.library.add_book(book)
        print(f"\nКнига успешно добавлена: {book}")
        print(f"Всего книг в библиотеке: {len(self.library.books)}")

    def remove_book(self):
        print("УДАЛЕНИЕ КНИГИ")
        print("-" * 80)

        if len(self.library.books) == 0:
            print("Библиотека пуста")
            return

        print(f"Всего книг в библиотеке: {len(self.library.books)}\n")
        for i, book in enumerate(self.library.books, 1):
            print(f"{i:3}. {book}")
            print(f"     ISBN: {book.isbn}, Жанр: {book.genre}")

        print("\n" + "-" * 80)
        print("Введите номер книги для удаления или '0' для возврата в меню")
        print("-" * 80)

        book_found = False
        book = None
        while not book_found:
            choice = input("\nВаш выбор: ").strip()

            if choice == "0":
                print("Возврат в главное меню")
                return

            if not choice:
                print("Выбор не может быть пустым, попробуйте снова")
                continue

            try:
                index = int(choice)
            except ValueError:
                print("Введите число, попробуйте снова")
                continue

            if index < 1 or index > len(self.library.books):
                print(f"Номер должен быть от 1 до {len(self.library.books)}, попробуйте снова")
                continue

            book = self.library.books[index - 1]
            book_found = True

        confirmed = False
        while not confirmed:
            print(f"\nВыбрана книга: {book}")
            print(f"ISBN: {book.isbn}")
            confirm = input("Удалить эту книгу? (да/нет): ").strip().lower()

            if confirm == "да":
                self.library.remove_book(book)
                print(f"\nКнига удалена: {book}")
                print(f"Осталось книг в библиотеке: {len(self.library.books)}")
                confirmed = True
            elif confirm == "нет":
                print("\nУдаление отменено")
                confirmed = True
            else:
                print("Неверный ответ, введите 'да' или 'нет'")

    def show_all_books(self):
        print("СПИСОК ВСЕХ КНИГ")
        print("-" * 80)

        if len(self.library.books) == 0:
            print("Библиотека пуста")
            return

        print(f"Всего книг: {len(self.library.books)}\n")
        for i, book in enumerate(self.library.books, 1):
            print(f"{i:3}. {book}")
            print(f"     ISBN: {book.isbn}, Жанр: {book.genre}")

    def search_by_isbn(self):
        print("ПОИСК ПО ISBN")
        print("-" * 80)
        print("Введите '0' для возврата в главное меню")
        print()

        found = False
        while not found:
            isbn = ""
            while not isbn:
                isbn = input("Введите ISBN: ").strip()

                if isbn == "0":
                    print("Возврат в главное меню")
                    return

                if not isbn:
                    print("ISBN не может быть пустым, попробуйте снова")

            book = self.library.search_by_isbn(isbn)

            if book:
                print("\nКнига найдена:")
                print_book_details(book)
                found = True
            else:
                print("\nКниг не найдено")
                print("Попробуйте ещё раз или введите 0, чтобы перейти в главное меню\n")

    def search_by_author(self):
        print("ПОИСК ПО АВТОРУ")
        print("-" * 80)
        print("Введите '0' для возврата в главное меню")
        print()

        found = False
        while not found:
            author = ""
            while not author:
                author = input("Введите имя автора: ").strip()

                if author == "0":
                    print("Возврат в главное меню")
                    return

                if not author:
                    print("Имя автора не может быть пустым, попробуйте снова")

            results = self.library.search_by_author(author)

            if len(results) > 0:
                print(f"\nНайдено книг: {len(results)}")
                print()
                for i, book in enumerate(results, 1):
                    print(f"{i}. {book}")
                found = True
            else:
                print("\nКниг не найдено")
                print("Попробуйте ещё раз или введите 0, чтобы перейти в главное меню\n")

    def search_by_year(self):
        print("ПОИСК ПО ГОДУ")
        print("-" * 80)
        print("Введите '0' для возврата в главное меню")
        print()

        found = False
        while not found:
            year = None
            while year is None:
                year_str = input("Введите год: ").strip()

                if year_str == "0":
                    print("Возврат в главное меню")
                    return

                if not year_str:
                    print("Год не может быть пустым, попробуйте снова")
                    continue

                try:
                    year = int(year_str)
                except ValueError:
                    print("Год должен быть числом, попробуйте снова")

            results = self.library.search_by_year(year)

            if len(results) > 0:
                print(f"\nНайдено книг: {len(results)}")
                print()
                for i, book in enumerate(results, 1):
                    print(f"{i}. {book}")
                found = True
            else:
                print("\nКниг не найдено")
                print("Попробуйте ещё раз или введите 0, чтобы перейти в главное меню\n")

    def search_by_genre(self):
        print("ПОИСК ПО ЖАНРУ")
        print("-" * 80)
        print("Введите '0' для возврата в главное меню")
        print()

        found = False
        while not found:
            genre = ""
            while not genre:
                genre = input("Введите жанр: ").strip()

                if genre == "0":
                    print("Возврат в главное меню")
                    return

                if not genre:
                    print("Жанр не может быть пустым, попробуйте снова")

            results = self.library.search_by_genre(genre)

            if len(results) > 0:
                print(f"\nНайдено книг: {len(results)}")
                print()
                for i, book in enumerate(results, 1):
                    print(f"{i}. {book}")
                found = True
            else:
                print("\nКниг не найдено")
                print("Попробуйте ещё раз или введите 0, чтобы перейти в главное меню\n")

    def exit_program(self):
        print("До свидания!")
        print(f"Финальная статистика: {self.library}")


def main():
    cli = CLI()
    try:
        cli.run()
    except KeyboardInterrupt:
        print("\n\nПрограмма прервана пользователем")
    except Exception as e:
        print(f"\nПроизошла ошибка: {e}")


if __name__ == "__main__":
    main()
