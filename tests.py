import pytest # pytest -v tests.py pytest -s tests.py

from main import BooksCollector

class TestBooksCollector:

    @pytest.fixture
    def collector(self):
        return BooksCollector()
    
    # № 1.0 добавление книг валид. add_new_book
    @pytest.mark.parametrize('book', ['К','Книга',
        'КнигаКнигаКнигаКнигаКнигаКнигаКнигаКнига',]) #40
    
    def test_add_new_book_val(self, collector, book):
        collector.add_new_book(book)
        
        assert book in collector.books_genre # или через assert len(collector.get_books_genre()) == 1
        
    # № 1.1 добавление книг невалид. add_new_book
    @pytest.mark.parametrize('book', ['',
        'КнигаКнигаКнигаКнигаКнигаКнигаКнигаКнига!']) #>41
    
    def test_add_new_book_inval(self, collector, book):
        
        collector.add_new_book(book)
        assert book not in collector.books_genre

    # № 1.2 добавление книг дубль. add_new_book
    @pytest.mark.parametrize('book', ['Книга1','Книга1'])
    def test_add_new_book_does_not_add_duplicate(self, collector, book):
        count= len(collector.books_genre)

        # 1 раз -добавил
        collector.add_new_book(book)
        assert book in collector.books_genre
        assert len(collector.books_genre) == count + 1

        # 2раз — добавил
        collector.add_new_book(book)
        count= len(collector.books_genre)
        assert count == 1  

    # № 2 устанавливаем книге жанр в списке set_book_genre
    @pytest.mark.parametrize('book, genre', [('Книга1', 'Ужасы'), ('Книга2', 'Фантастика')])
    def test_set_book_genre_to_book(self, collector, book, genre):
        
        collector.add_new_book(book)
        collector.set_book_genre(book, genre)
        
        assert book in collector.books_genre

        loc= collector.books_genre.get(book)
        assert loc == genre

    # № 3 # получаем жанр книги по её имени get_book_genre
    @pytest.mark.parametrize('book, genre', [('Книга1', 'Ужасы'), ('Книга2', 'Фантастика')])
    def test_get_book_genre_out_genre(self, collector, book, genre):
        
        collector.books_genre[book] = genre

        loc= collector.get_book_genre(book)
        assert loc == genre    

    # № 4 # выводим список книг с определённым жанром get_books_with_specific_genre
    def test_get_books_with_specific_genre_by_genre(self, collector):
        book= ['Книга1', 'Книга2']
        genre= 'Фантастика'

        for name in book:
            collector.add_new_book(name)
            collector.set_book_genre(name, genre)

        book_v_genre = collector.get_books_with_specific_genre(genre)
       
        assert book_v_genre == book

    # № 5 # получаем словарь books_genre
    def test_get_books_genre_pustoi(self,collector):

        assert collector.get_books_genre() == {}

    # № 5.1 # получаем словарь books_genre через заполнение
    def test_get_books_genre_no_pustoi(self, collector):
        collector.add_new_book('Книга1')
        collector.set_book_genre('Книга1', 'Фантастика')
        assert collector.get_books_genre() == {'Книга1': 'Фантастика'}

    # № 6 возвращаем книги, подходящие детям get_books_with_specific_genre
    @pytest.mark.parametrize(
        'book, genre',[
            ('Книга1', 'Фантастика'),
            ('Книга2', 'Мультфильмы'),
            ('Книга3', 'Комедии')])
    def test_get_books_for_children_val(self,collector, book, genre):
        
        collector.add_new_book(book)
        collector.set_book_genre(book, genre)

        assert book in collector.get_books_for_children()

    # № 6.1 возвращаем книги, подходящие детям get_books_with_specific_genre
    @pytest.mark.parametrize('book, genre', [
        ('Книга1', 'Фантастика'),
        ('Книга2', 'Ужасы'),        # не детская
        ('Книга3', 'Детективы')])   # не детская
    def test_get_books_for_children_i_no_val(self, collector, book, genre):
    
        collector.add_new_book(book)
        collector.set_book_genre(book, genre)
        res= collector.get_books_for_children()

        assert (book in res) == (genre not in collector.genre_age_rating)

    # № 7 добавляем книгу в Избранное add_book_in_favorites
    def test_add_book_in_favorites_new_book_add(self,collector):

        collector.add_new_book('Книга1')
       
        assert 'Книга1' in collector.books_genre

        collector.add_book_in_favorites('Книга1')

        favorites = collector.get_list_of_favorites_books()
        assert 'Книга1' in favorites
       

    # № 7.1 добавляем книгу в Избранное повторно  add_book_in_favorites    
    def test_add_book_in_favorites_two_book_add(self,collector):

        collector.add_new_book('Книга1')
        
        collector.add_book_in_favorites('Книга1') # 1 раз
        collector.add_book_in_favorites('Книга1') # 2 раз
        
        favorites= collector.get_list_of_favorites_books()
        assert 'Книга1' in favorites

     # № 8.0  # удаляем книгу из Избранного delete_book_from_favorites
    def test_delete_book_from_favorites_book_in_favorites_book_rm(self,collector):

        collector.add_new_book('Книга1')
        collector.add_book_in_favorites('Книга1')

        collector.delete_book_from_favorites('Книга1')

        favorites= collector.get_list_of_favorites_books()
        assert 'Книга1' not in favorites

    # № 9.0 # получаем список Избранных книг get_list_of_favorites_books
    def test_get_list_of_favorites_list_all_favorite_books(self,collector):

        collector.add_new_book('Книга1')
        collector.add_new_book('Книга2')

        collector.add_book_in_favorites('Книга1')
        collector.add_book_in_favorites('Книга2')

        assert collector.get_list_of_favorites_books() == ['Книга1', 'Книга2']
      
       


