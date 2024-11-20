import unittest
from library_manager import add_book, \
    remove_book, \
    search_books, \
    Book, \
    load_library, \
    save_library, \
    update_book_status  # Импортируем функцию update_book_status

# Используем отдельный файл для тестов
TEST_FILE = "test_library.json"

class TestLibraryManager(unittest.TestCase):
    """
    Класс для тестирования функций работы с библиотекой книг.
    Тесты работают с временным файлом, чтобы не изменять данные в основной библиотеке.
    """

    def setUp(self):
        """
        Этот метод вызывается перед каждым тестом.
        Он очищает библиотеку в тестовом файле, чтобы каждый тест был независим.
        """
        save_library([], TEST_FILE)  # Очищаем тестовый файл перед каждым тестом

    def test_add_book(self):
        """
        Тестируем функцию добавления книги.
        Проверяем, что книга добавляется в библиотеку и сохраняется в тестовом файле.
        """
        initial_books = load_library(TEST_FILE)
        add_book("Test Book", "Test Author", 2024, TEST_FILE)
        books_after_add = load_library(TEST_FILE)

        self.assertGreater(len(books_after_add), len(initial_books), "Книга не добавлена.")  # Проверяем, что книга добавлена

        # Проверяем, что добавленная книга имеет правильные данные
        new_book = books_after_add[-1]
        self.assertEqual(new_book.title, "Test Book")
        self.assertEqual(new_book.author, "Test Author")
        self.assertEqual(new_book.year, 2024)

    def test_remove_book(self):
        """
        Тестируем функцию удаления книги.
        Проверяем, что книга удаляется из библиотеки по её ID.
        """
        add_book("Book to Remove", "Test Author", 2024, TEST_FILE)
        books_after_add = load_library(TEST_FILE)
        book_to_remove = books_after_add[-1]
        book_id = book_to_remove.id

        remove_book(book_id, TEST_FILE)
        books_after_remove = load_library(TEST_FILE)

        self.assertNotIn(book_to_remove, books_after_remove, "Книга не была удалена.")  # Книга должна быть удалена

    def test_search_books_by_title(self):
        """
        Тестируем поиск книг по названию.
        Проверяем, что поиск по названию возвращает правильную книгу.
        """
        add_book("Book One", "Author One", 2022, TEST_FILE)
        add_book("Book Two", "Author Two", 2023, TEST_FILE)

        results = search_books(title="Book One", file_path=TEST_FILE)
        self.assertEqual(len(results), 1, "Найдено больше одной книги при поиске по названию.")
        self.assertEqual(results[0].title, "Book One")

    def test_search_books_by_author(self):
        """
        Тестируем поиск книг по автору.
        Проверяем, что поиск по автору возвращает правильное количество книг.
        """
        add_book("Book One", "Author One", 2022, TEST_FILE)
        add_book("Book Two", "Author One", 2023, TEST_FILE)

        results = search_books(author="Author One", file_path=TEST_FILE)
        self.assertEqual(len(results), 2, "Найдено неверное количество книг при поиске по автору.")

    def test_update_book_status(self):
        """
        Тестируем изменение статуса книги.
        Проверяем, что статус книги изменяется на "выдана".
        """
        add_book("Test Book", "Test Author", 2024, TEST_FILE)
        books = load_library(TEST_FILE)
        book_to_update = books[-1]
        book_id = book_to_update.id

        # Изменяем статус книги на "выдана"
        update_success = update_book_status(book_id, "выдана", TEST_FILE)
        self.assertTrue(update_success, "Статус книги не был изменён на 'выдана'.")

        # Проверяем, что статус действительно изменился
        updated_books = load_library(TEST_FILE)
        updated_book = updated_books[-1]
        self.assertEqual(updated_book.status, "выдана", "Статус книги не был обновлён.")

    def tearDown(self):
        """
        Этот метод вызывается после каждого теста.
        Он удаляет временный файл, используемый для тестирования, чтобы не оставлять мусор в системе.
        """
        import os
        os.remove(TEST_FILE)  # Удаляем тестовый файл после завершения тестов


if __name__ == "__main__":
    unittest.main()
