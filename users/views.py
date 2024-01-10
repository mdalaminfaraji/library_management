from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from .models import  UserProfile
from .forms import  UserRegistrationForm, ChangeUserData, DepositForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

from books.models import BorrowedBook
# Create your views here.
from django.core.mail import  EmailMultiAlternatives
from django.template.loader import render_to_string


def Register(request):
        if request.method=="POST":
                form=UserRegistrationForm(request.POST)
                if form.is_valid():
                        user=form.save()
                        UserProfile.objects.create(user=user)
                        login(request, user)
                        
                        messages.success(request, 'Register successfully done')
                        return redirect("home")
        else:
                form=UserRegistrationForm()
                
        return render(request, "register.html", {"form":form, 'type':'Register'})



def SignUP(request):
    if request.method=='POST':
        form=AuthenticationForm(request, request.POST)
        if form.is_valid():
            user_name=form.cleaned_data['username']
            user_pass=form.cleaned_data['password']
            user=authenticate(username=user_name, password=user_pass)
            if user is not None:
                messages.success(request, 'Login successfully done')
                login(request, user)
                return redirect('profile')
            else:
                messages.warning(request, 'user do not find please  login')
                return  redirect('register')
          
    else:
        form=AuthenticationForm()
        return render(request, 'register.html', {'form':form, 'type':'login'})

@login_required
def profile(request):
        userprofile = UserProfile.objects.get(user=request.user)
        borrowed_books = BorrowedBook.objects.filter(user=request.user)
        return render(request, 'profile.html', {"data":request.user, "borrowed_books":borrowed_books, "userprofile":userprofile})


@login_required
def edit_profile(request):
    if request.method=="POST":
        profile_form=ChangeUserData(request.POST, instance=request.user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile updated successfully done')
            return redirect('profile')
    else:
        profile_form = ChangeUserData( instance=request.user)
    return render(request, 'update_profile.html', {'form':profile_form, 'type':'Profile', "user":request.user})

@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


def send_transaction_email(user, amount, subject, template):
        message = render_to_string(template, {
            'user' : user,
            'amount' : amount,
        })
        send_email = EmailMultiAlternatives(subject, '', to=[user.email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()

@login_required
def deposit_money(request):
    user_profile = UserProfile.objects.get(user=request.user)

    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            user_profile.deposit_amount += amount
            user_profile.save()

            # Send deposit success email to the user
            send_transaction_email(request.user, amount, "Deposit Message", "deposit_email.html")
            messages.success(request, f'{"{:,.2f}".format(float(amount))} was deposited to your account successfully')
        
    else:
        form = DepositForm()

    return render(request, 'deposit_money.html', {'form': form, 'user_profile': user_profile})


def view_user_deposit(request):
    user_profile = request.user.userprofile

    # Access the deposit_amount
    deposit_amount = request.user.userprofile.deposit_amount

    return render(request, 'view_deposit.html', {'deposit_amount': deposit_amount})


@login_required
def borrowing_history(request):
    borrowed_books = BorrowedBook.objects.filter(user=request.user)

    return render(request, 'profile.html', {'borrowed_books': borrowed_books})

@login_required
def returnBook(request, book_id):
    borrowed_book = get_object_or_404(BorrowedBook, user=request.user, book_id=book_id, returned=False)
    book = borrowed_book.book

    if request.method == 'POST':
        # Process returning logic
        borrowed_book.returned = True
        borrowed_book.save()

        user_profile = UserProfile.objects.get(user=request.user)
        user_profile.deposit_amount += book.borrowing_price
        user_profile.save()

        messages.success(request, 'Return Book successfully done')

        return redirect('profile')
    else:
        # Add a response for non-POST requests (e.g., redirect to another page)
        return redirect('profile')

    # return render(request, 'profile.html', {'book': book, 'borrowed_book': borrowed_book})

