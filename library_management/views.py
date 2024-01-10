from django.shortcuts import render
from books.models import Book,Category

def home(request, category_slug=None):
        books = Book.objects.all()
        if category_slug is not None:
                category=Category.objects.get(slug=category_slug)
                books=Book.objects.filter(category=category)
        allCategory=Category.objects.all()
        return render(request, "home.html",{'books': books, "allCategory":allCategory})