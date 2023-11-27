from django.db import models


class Author(models.Model):
    # CharField - предназначен для коротких строк фиксированной длины.
    name = models.CharField(max_length=50)
    # TextField - предназначен для длинных текстовых данных.
    bio = models.TextField()

    def __str__(self):
        return self.name
