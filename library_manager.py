import json
from typing import List, Optional, Dict

# Определяем файл для хранения данных библиотеки
LIBRARY_FILE = "library.json"

# Структура книги
class Book:
    """
    Класс для представления книги в библиотеке.

    Атрибуты:
        id (int): Уникальный идентификатор книги.
        title (str): Название книги.
        author (str): Автор книги.
        year (int): Год издания книги.
        status (str): Статус книги (по умолчанию "в наличии").
    """
    def __init__(self, id: int, title: str, author: str, year: int, status: str = "в наличии"):
        """
        Инициализирует объект книги.

        :param id: Уникальный идентификатор книги.
        :param title: Название книги.
        :param author: Автор книги.
        :param year: Год издания книги.
        :param status: Статус книги, по умолчанию "в наличии".
        """
        self.id: int = id
        self.title: str = title
        self.author: str = author
        self.year: int = year
        self.status: str = status

    def to_dict(self) -> Dict[str, str]:
        """
        Преобразует объект книги в словарь.

        :return: Словарь с данными книги.
        """
        return {
            "id": str(self.id),
            "title": self.title,
            "author": self.author,
            "year": str(self.year),
            "status": self.status
        }

    @staticmethod
    def from_dict(data: Dict[str, str]) -> 'Book':
        """
        Создаёт объект книги из словаря.

        :param data: Словарь с данными книги.
        :return: Объект книги.
        """
        return Book(
            id=int(data["id"]),
            title=data["title"],
            author=data["author"],
            year=int(data["year"]),
            status=data["status"]
        )


# Утилиты для работы с файлами
def load_library(file_path: str) -> List[Book]:
    """
    Загружает библиотеку книг из файла.

    :param file_path: Путь к файлу, из которого загружаются книги.
    :return: Список объектов книг, загруженных из файла.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return [Book.from_dict(book) for book in json.load(file)]
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_library(books: List[Book], file_path: str) -> None:
    """
    Сохраняет список книг в файл.

    :param books: Список объектов книг, которые нужно сохранить в файл.
    :param file_path: Путь к файлу, в который нужно сохранить данные.
    """
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump([book.to_dict() for book in books], file, ensure_ascii=False, indent=4)
    print(f"Данные записаны в {file_path}.")


# Операции с библиотекой
def add_book(title: str, author: str, year: int, file_path: str) -> Book:
    """
    Добавляет книгу в библиотеку.

    :param title: Название книги.
    :param author: Автор книги.
    :param year: Год издания книги.
    :param file_path: Путь к файлу, где хранится библиотека.
    :return: Объект добавленной книги.
    """
    books = load_library(file_path)
    new_id = max((book.id for book in books), default=0) + 1
    new_book = Book(id=new_id, title=title, author=author, year=year)
    books.append(new_book)
    save_library(books, file_path)
    return new_book


def remove_book(book_id: int, file_path: str) -> bool:
    """
    Удаляет книгу по её ID.

    :param book_id: ID книги, которую нужно удалить.
    :param file_path: Путь к файлу, где хранится библиотека.
    :return: True, если книга была удалена, иначе False.
    """
    books = load_library(file_path)
    filtered_books = [book for book in books if book.id != book_id]
    if len(filtered_books) == len(books):  # Если книга не найдена
        return False
    save_library(filtered_books, file_path)
    return True


def search_books(file_path: str, title: Optional[str] = None, author: Optional[str] = None, year: Optional[int] = None) -> List[Book]:
    """
    Ищет книги по названию, автору или году.

    :param file_path: Путь к файлу, где хранится библиотека.
    :param title: Название книги (поиск по частичному совпадению).
    :param author: Автор книги (поиск по частичному совпадению).
    :param year: Год издания книги.
    :return: Список книг, соответствующих критериям поиска.
    """
    books = load_library(file_path)
    results = books
    if title:
        results = [book for book in results if title.lower() in book.title.lower()]
    if author:
        results = [book for book in results if author.lower() in book.author.lower()]
    if year:
        results = [book for book in results if book.year == year]
    return results


def list_books(file_path: str) -> List[Book]:
    """
    Возвращает список всех книг в библиотеке.

    :param file_path: Путь к файлу, где хранится библиотека.
    :return: Список всех книг.
    """
    return load_library(file_path)


def update_book_status(book_id: int, status: str, file_path: str) -> bool:
    """
    Обновляет статус книги (например, 'в наличии' или 'выдана').

    :param book_id: ID книги, для которой нужно изменить статус.
    :param status: Новый статус книги.
    :param file_path: Путь к файлу, где хранится библиотека.
    :return: True, если статус был успешно обновлён, иначе False.
    """
    if status not in ["в наличии", "выдана"]:
        raise ValueError("Invalid status. Use 'в наличии' or 'выдана'.")
    books = load_library(file_path)
    for book in books:
        if book.id == book_id:
            book.status = status
            save_library(books, file_path)
            return True
    return False


# Главный интерфейс программы
def main() -> None:
    """
    Основной интерфейс программы, который позволяет пользователю взаимодействовать с библиотекой.
    Он отображает меню и вызывает соответствующие функции в зависимости от выбора пользователя.
    """
    while True:
        print("\n--- Библиотека книг ---")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Искать книги")
        print("4. Показать все книги")
        print("5. Изменить статус книги")
        print("6. Выход")

        choice = input("Выберите действие (1-6): ")
        try:
            if choice == "1":
                title = input("Введите название книги: ")
                author = input("Введите автора книги: ")
                year = int(input("Введите год издания: "))
                new_book = add_book(title, author, year, LIBRARY_FILE)
                print(f"Книга добавлена: {new_book.to_dict()}")
            elif choice == "2":
                book_id = int(input("Введите ID книги для удаления: "))
                if remove_book(book_id, LIBRARY_FILE):
                    print("Книга удалена.")
                else:
                    print("Книга с таким ID не найдена.")
            elif choice == "3":
                title = input("Введите название книги (или оставьте пустым): ")
                author = input("Введите автора книги (или оставьте пустым): ")
                year_input = input("Введите год издания (или оставьте пустым): ")
                year = int(year_input) if year_input else None
                results = search_books(LIBRARY_FILE, title=title, author=author, year=year)
                if results:
                    for book in results:
                        print(book.to_dict())
                else:
                    print("Книги не найдены.")
            elif choice == "4":
                books = list_books(LIBRARY_FILE)
                if books:
                    for book in books:
                        print(book.to_dict())
                else:
                    print("Библиотека пуста.")
            elif choice == "5":
                book_id = int(input("Введите ID книги для изменения статуса: "))
                status = input("Введите новый статус ('в наличии' или 'выдана'): ")
                if update_book_status(book_id, status, LIBRARY_FILE):
                    print("Статус книги обновлён.")
                else:
                    print("Книга с таким ID не найдена.")
            elif choice == "6":
                print("Выход из программы.")
                break
            else:
                print("Неверный выбор, попробуйте снова.")
        except ValueError as e:
            print(f"Ошибка ввода: {e}")
        except Exception as e:
            print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    finally:
        # Сохраняем библиотеку при выходе
        books = list_books(LIBRARY_FILE)
        save_library(books, LIBRARY_FILE)
        print("Изменения сохранены. Программа завершена.")
