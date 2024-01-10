from django.urls import path
from .views import  book_details, borrow_book, review_book


urlpatterns = [
    path('book-details/<int:book_id>/', book_details, name='book_details'),
    path('borrow/<int:book_id>/', borrow_book, name='borrow_book'),
    path('review/<int:book_id>/', review_book, name='review_book'),

]
