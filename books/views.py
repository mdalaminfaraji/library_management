from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import BorrowedBook, Book, BookReview, Category
from users.models import UserProfile
from .forms import BookReviewForm
from django.contrib import messages
from django.core.mail import  EmailMultiAlternatives
from django.template.loader import render_to_string

def book_details(request, book_id):
        book = get_object_or_404(Book, pk=book_id)
        reviews = BookReview.objects.filter(book=book)
        print(request.user.id, book_id)
        if request.user.is_authenticated :
                deposit_amount=request.user.userprofile.deposit_amount
                user_borrowed_book = BorrowedBook.objects.filter(user_id=request.user.id, book_id=book_id, returned=False)
                return render(request, 'book_details.html', {'book': book, 'reviews': reviews, 'deposit_amount':deposit_amount, 'user_borrowed_book': user_borrowed_book, 'form': BookReviewForm()})
        else:
                return render(request, 'book_details.html', {'book': book, 'reviews': reviews})
                

def send_transaction_email(user, amount, current_amount, subject, template):
        message = render_to_string(template, {
            'user' : user,
            'amount' : amount,
            "current_amount":current_amount,
        })
        send_email = EmailMultiAlternatives(subject, '', to=[user.email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()


@login_required
def borrow_book(request, book_id):
    if request.method == 'POST':
        book = Book.objects.get(pk=book_id)
        user = request.user
        userprofile = UserProfile.objects.get(user=user)
        print(userprofile)
        if userprofile.deposit_amount >= book.borrowing_price:
            userprofile.deposit_amount -= book.borrowing_price
            userprofile.save()
            borrowed_book = BorrowedBook.objects.create(user=user, book=book)
            send_transaction_email(request.user, book.borrowing_price,userprofile.deposit_amount, "Borrow Message", "borrow_email.html")
            messages.success(request, f"You have successfully borrowed.")
            
            return redirect('book_details', book_id=book_id)
        else:
            messages.error(request, "Insufficient deposit amount to borrow the book.")
            return redirect('book_details', book_id=book_id)
    else:
        pass

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
    reviews = BookReview.objects.filter(book=book)
    deposit_amount=request.user.userprofile.deposit_amount
    user_borrowed_book = BorrowedBook.objects.filter(user_id=request.user.id, book_id=book_id, returned=False)
    if request.method == 'POST':
        form = BookReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.book = book
            review.save()

            return render(request, 'book_details.html', {'book': book, 'reviews': reviews,'deposit_amount':deposit_amount,  'user_borrowed_book': user_borrowed_book, 'form': BookReviewForm()})
        return render(request, 'book_details.html', {'book': book, 'reviews': reviews,'deposit_amount':deposit_amount,  'user_borrowed_book': user_borrowed_book, 'form': BookReviewForm()})

#     return render(request, 'book_details.html', {'book': book, 'form': form})


