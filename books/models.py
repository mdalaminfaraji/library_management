from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug=models.SlugField(max_length=100, unique=True, null=True,blank=True)
    def __str__(self):
            return self.name

class Book(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='books/media/uploads/',blank=True, null=True)
    borrowing_price = models.DecimalField(max_digits=10, decimal_places=2)
    reviews = models.ManyToManyField(User, through='BookReview')
    categories = models.ManyToManyField(Category)
    def __str__(self):
        return self.name

class BookReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    review = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    

