import pytest
from books_collector import BooksCollector


# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector

class TestBooksCollector:

    @pytest.fixture(autouse=True)
    def books_collector(self):
        self.collector = BooksCollector()
        return self.collector

    # тестируем метод add_new_book для добавления новой книги
    # и метода get_books_genre для получения списка добавленных книг
    def test_add_new_book_and_check_list(self):
        book_name = "Человек-невидимка"
        self.collector.add_new_book(book_name)

        assert book_name in self.collector.get_books_genre()

    @pytest.mark.parametrize('book_name', ['', 'Странная история доктора Джекила и мистера Хайда'])
    def test_add_new_book_long_and_blank_names_not_added(self, book_name):
        self.collector.add_new_book(book_name)

        assert book_name not in self.collector.get_books_genre()

    def test_add_new_book_add_two_books(self):
        self.collector.add_new_book('Гордость и предубеждение и зомби')
        self.collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        assert len(self.collector.get_books_genre()) == 2

    # тестирование метода set_book_genre для добавления жанра книги
    # тестирование метода get_book_genre для получения жанра книги по названию

    def test_set_book_genre_and_get_gender_by_name(self):
        self.collector.add_new_book('Мохнатая Азбука')
        self.collector.set_book_genre("Мохнатая Азбука", "Мультфильмы")

        assert self.collector.get_book_genre("Мохнатая Азбука") == "Мультфильмы"

    def test_set_book_genre_unknown_name_not_found(self):
        self.collector.add_new_book('Человек-невидимка')
        self.collector.set_book_genre("Человек-невидимка", "Фантастика")

        assert self.collector.get_book_genre("невидимка") is None

    # тестирование метода get_books_with_specific_genre для получения книг по конкретному жанру

    def test_get_books_with_specific_genre_by_book_name(self):
        self.collector.add_new_book("Трое в лодке, не считая собаки")
        self.collector.set_book_genre("Трое в лодке, не считая собаки", "Комедии")

        assert self.collector.get_books_with_specific_genre("Комедии") == ["Трое в лодке, не считая собаки"]

    @pytest.mark.parametrize('genre_name', ['', 'Комедия'])
    def test_get_books_with_specific_genre_unknown_and_blank_genre_not_found(self, genre_name):
        self.collector.add_new_book("Трое в лодке, не считая собаки")
        self.collector.set_book_genre("Трое в лодке, не считая собаки", "Комедии")

        assert self.collector.get_books_with_specific_genre(genre_name) == []

    def test_get_books_with_specific_genre_not_added_genre_not_found(self):
        self.collector.add_new_book("Понедельник начинается в субботу")
        self.collector.set_book_genre("Понедельник начинается в субботу", "Фантастика")

        assert self.collector.get_books_with_specific_genre("Ужасы") == []

    def test_get_books_with_specific_genre_two_genre_added(self):
        self.collector.add_new_book("Сто лет тому вперед")
        self.collector.set_book_genre("Сто лет тому вперед", "Фантастика")
        self.collector.add_new_book("Понедельник начинается в субботу")
        self.collector.set_book_genre("Понедельник начинается в субботу", "Фантастика")

        assert len(self.collector.get_books_with_specific_genre("Фантастика")) == 2

    # тестирование метода get_books_for_children для получения списка книг для детей

    def test_get_books_for_children(self):
        self.collector.add_new_book("Баранкин, будь человеком")
        self.collector.set_book_genre("Баранкин, будь человеком", "Комедии")
        self.collector.add_new_book("Тяпа, Борька и ракета")
        self.collector.set_book_genre("Тяпа, Борька и ракета", "Мультфильмы")
        self.collector.add_new_book("ОНО")
        self.collector.set_book_genre("ОНО", "Ужасы")
        self.collector.add_new_book("Этюд в багровых тонах")
        self.collector.set_book_genre("Этюд в багровых тонах", "Детективы")
        self.collector.add_new_book("Понедельник начинается в субботу")
        self.collector.set_book_genre("Понедельник начинается в субботу", "Фантастика")

        assert self.collector.get_books_for_children() == ['Баранкин, будь человеком', 'Тяпа, Борька и ракета',
                                                           'Понедельник начинается в субботу']

    # тестирование метода add_book_in_favorites для добавления книг в избранное

    def test_add_book_in_favorites_new_added_book(self):
        self.collector.add_new_book("Сирены Тинана")
        self.collector.set_book_genre("Сирены Тинана", "Фантастика")

        self.collector.add_book_in_favorites("Сирены Тинана")
        assert "Сирены Тинана" in self.collector.get_list_of_favorites_books()

    def test_add_book_in_favorites_not_added_book_not_in_list(self):
        self.collector.add_book_in_favorites("Всем привет")
        assert "Всем привет" not in self.collector.get_list_of_favorites_books()

    # тестирование метода delete_book_from_favorites для удаления книг из избранного

    def delete_book_from_favorites_book_deleted(self):
        self.collector.add_new_book("Сирены Тинана")
        self.collector.add_new_book("Собака Баскервилей")

        self.collector.add_book_in_favorites("Сирены Тинана")
        self.collector.add_book_in_favorites("Собака Баскервилей")

        self.collector.delete_book_from_favorites("Собака Баскервилей")
        assert "Сирены Тинана" in self.collector.get_list_of_favorites_books()
        assert "Собака Баскервилей" not in self.collector.get_list_of_favorites_books()

    # тестирование метода get_list_of_favorites_books для получения списка избранных книг

    def get_list_of_favorites_books_get_two_books(self):
        self.collector.add_new_book("Сирены Тинана")
        self.collector.set_book_genre("Сирены Тинана", "Фантастика")
        self.collector.add_new_book("Дверь в лето")
        self.collector.set_book_genre("Дверь в лето", "Фантастика")

        assert len(self.collector.get_list_of_favorites_books()) == 2
