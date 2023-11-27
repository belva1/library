from django.db import models
from books.models import Book
from users.models import UserModel


class Status(models.TextChoices):
    PENDING = "Pending"
    APPROVED = "Approved"
    COLLECTED = "Collected"
    COMPLETE = "Complete"
    DECLINED = "Declined"


class BorrowRequestModel(models.Model):
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)  # if delete one book, then deleted all BorrowRequests
    borrower = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True, blank=True)
    overdue = models.BooleanField(default=False)
    request_date = models.DateField()
    approval_date = models.DateField(null=True, blank=True)
    due_date = models.DateField(null=True, blank=True)
    complete_date = models.DateField(null=True, blank=True)
