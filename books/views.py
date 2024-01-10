from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import BorrowedBook, Book, BookReview, Category
from users.models import UserProfile
from .forms import BookReviewForm


def book_details(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    reviews = BookReview.objects.filter(book=book)
    return render(request, 'book_details.html', {'book': book, 'reviews': reviews})


@login_required
def borrow_book(request, book_id):
    book = Book.objects.get(pk=book_id)
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        # Process borrowing logic and send email

        return redirect('book_list')

    return render(request, 'borrow_book.html', {'book': book, 'user_profile': user_profile})

@login_required
def return_book(request, book_id):
    book = Book.objects.get(pk=book_id)
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        # Process returning logic and send email

        return redirect('book_list')

    return render(request, 'return_book.html', {'book': book, 'user_profile': user_profile})

@login_required
def review_book(request, book_id):
    book = Book.objects.get(pk=book_id)
    form = BookReviewForm()

    if request.method == 'POST':
        form = BookReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.book = book
            review.save()

            return redirect('book_list')

    return render(request, 'review_book.html', {'book': book, 'form': form})

@login_required
def borrowing_history(request):
    borrowed_books = BorrowedBook.objects.filter(user=request.user)

    return render(request, 'borrowing_history.html', {'borrowed_books': borrowed_books})
