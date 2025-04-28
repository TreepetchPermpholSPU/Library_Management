from django.db import models
from django.utils import timezone

class Book(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('rented', 'Rented'),
        ('damaged', 'Damaged'),
        ('lost', 'Lost'),
    ]
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    category = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')

    def __str__(self):
        return self.title

class Member(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return self.name

class Rental(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    rent_date = models.DateField(default=timezone.now)
    due_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    fine = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.member.name} - {self.book.title}"
