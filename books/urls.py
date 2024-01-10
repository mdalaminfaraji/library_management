from django.urls import path
from .views import  borrowing_history, book_details


urlpatterns = [
    path('borrowing-history/', borrowing_history, name='borrowing_history'),
     path('book-details/<int:book_id>/', book_details, name='book_details'),

]
