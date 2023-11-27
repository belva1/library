from django.db import models
from authors.models import Author
from genres.models import Genre
from users.models import UserModel


class Book(models.Model):
    title = models.CharField(max_length=50, unique=True)
    summary = models.TextField()
    isbn = models.CharField(max_length=13, unique=True)
    available = models.BooleanField(default=True)
    published_date = models.DateField()
    publisher = models.CharField(max_length=50)
    genre = models.ManyToManyField(Genre, blank=False)
    authors = models.ManyToManyField(Author)
    # Юзер, который берет книгу из библиотеки
    borrower = models.OneToOneField(UserModel, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title
