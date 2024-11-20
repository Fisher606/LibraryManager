import unittest
from library_manager import add_book, \
    remove_book, \
    search_books, \
    Book, \
    load_library, \
    save_library, \
    update_book_status  # Импортируем функцию update_book_status

class TestLibraryManager(unittest.TestCase):

    def setUp(self):
        """Этот метод вызывается перед каждым тестом. Он очищает библиотеку."""
        # Сначала очищаем библиотеку, чтобы каждый тест был независим.
        save_library([])

    def test_add_book(self):
        """Тестируем функцию добавления книги"""
        initial_books = load_library()
        add_book("Test Book", "Test Author", 2024)
        books_after_add = load_library()

        self.assertGreater(len(books_after_add),
                           len(initial_books))  # Проверяем, что книга добавлена

        # Проверяем, что добавленная книга имеет правильные данные
        new_book = books_after_add[-1]
        self.assertEqual(new_book.title, "Test Book")
        self.assertEqual(new_book.author, "Test Author")
        self.assertEqual(new_book.year, 2024)

    def test_remove_book(self):
        """Тестируем функцию удаления книги"""
        add_book("Book to Remove", "Test Author", 2024)
        books_after_add = load_library()
        book_to_remove = books_after_add[-1]
        book_id = book_to_remove.id

        remove_book(book_id)
        books_after_remove = load_library()

        self.assertNotIn(book_to_remove, books_after_remove)  # Книга должна быть удалена

    def test_search_books_by_title(self):
        """Тестируем поиск книг по названию"""
        add_book("Book One", "Author One", 2022)
        add_book("Book Two", "Author Two", 2023)

        results = search_books(title="Book One")
        self.assertEqual(len(results), 1)  # Должна быть найдена только 1 книга
        self.assertEqual(results[0].title, "Book One")

    def test_search_books_by_author(self):
        """Тестируем поиск книг по автору"""
        add_book("Book One", "Author One", 2022)
        add_book("Book Two", "Author One", 2023)

        results = search_books(author="Author One")
        self.assertEqual(len(results), 2)  # Должны быть найдены обе книги с таким автором

    def test_update_book_status(self):
        """Тестируем изменение статуса книги"""
        add_book("Test Book", "Test Author", 2024)
        books = load_library()
        book_to_update = books[-1]
        book_id = book_to_update.id

        # Изменяем статус книги на "выдана" (правильный вызов функции)
        update_success = update_book_status(book_id, "выдана")
        self.assertTrue(update_success)  # Проверяем, что статус был изменён

        # Проверяем, что статус действительно изменился
        updated_books = load_library()
        updated_book = updated_books[-1]
        self.assertEqual(updated_book.status, "выдана")


if __name__ == "__main__":
    unittest.main()
