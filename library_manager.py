import json
from typing import List, Optional, Dict

# Define the file to store library data
LIBRARY_FILE = "library.json"

# Book structure
class Book:
    def __init__(self, id: int, title: str, author: str, year: int, status: str = "в наличии"):
        self.id = id
        self.title = title
        self.author = author
        self.year = year
        self.status = status

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status
        }

    @staticmethod
    def from_dict(data: Dict):
        return Book(
            id=data["id"],
            title=data["title"],
            author=data["author"],
            year=data["year"],
            status=data["status"]
        )


# Utility functions for file handling
def load_library() -> List[Book]:
    try:
        with open(LIBRARY_FILE, "r", encoding="utf-8") as file:
            return [Book.from_dict(book) for book in json.load(file)]
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_library(books: List[Book]) -> None:
    with open(LIBRARY_FILE, "w", encoding="utf-8") as file:
        json.dump([book.to_dict() for book in books], file, ensure_ascii=False, indent=4)
    print("Данные записаны в library.json.")  # Выводим сообщение, что данные сохранены


# Library operations
def add_book(title: str, author: str, year: int) -> Book:
    books = load_library()
    new_id = max((book.id for book in books), default=0) + 1
    new_book = Book(id=new_id, title=title, author=author, year=year)
    books.append(new_book)
    save_library(books)
    return new_book


def remove_book(book_id: int) -> bool:
    books = load_library()
    filtered_books = [book for book in books if book.id != book_id]
    if len(filtered_books) == len(books):  # No book removed
        return False
    save_library(filtered_books)
    return True


def search_books(title: Optional[str] = None, author: Optional[str] = None, year: Optional[int] = None) -> List[Book]:
    books = load_library()
    results = books
    if title:
        results = [book for book in results if title.lower() in book.title.lower()]
    if author:
        results = [book for book in results if author.lower() in book.author.lower()]
    if year:
        results = [book for book in results if book.year == year]
    return results


def list_books() -> List[Book]:
    return load_library()


def update_book_status(book_id: int, status: str) -> bool:
    if status not in ["в наличии", "выдана"]:
        raise ValueError("Invalid status. Use 'в наличии' or 'выдана'.")
    books = load_library()
    for book in books:
        if book.id == book_id:
            book.status = status
            save_library(books)
            return True
    return False


# Main console interface
def main():
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
                new_book = add_book(title, author, year)
                print(f"Книга добавлена: {new_book.to_dict()}")
            elif choice == "2":
                book_id = int(input("Введите ID книги для удаления: "))
                if remove_book(book_id):
                    print("Книга удалена.")
                else:
                    print("Книга с таким ID не найдена.")
            elif choice == "3":
                title = input("Введите название книги (или оставьте пустым): ")
                author = input("Введите автора книги (или оставьте пустым): ")
                year_input = input("Введите год издания (или оставьте пустым): ")
                year = int(year_input) if year_input else None
                results = search_books(title=title or None, author=author or None, year=year)
                if results:
                    for book in results:
                        print(book.to_dict())
                else:
                    print("Книги не найдены.")
            elif choice == "4":
                books = list_books()
                if books:
                    for book in books:
                        print(book.to_dict())
                else:
                    print("Библиотека пуста.")
            elif choice == "5":
                book_id = int(input("Введите ID книги для изменения статуса: "))
                status = input("Введите новый статус ('в наличии' или 'выдана'): ")
                if update_book_status(book_id, status):
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
        books = list_books()
        save_library(books)
        print("Изменения сохранены. Программа завершена.")
