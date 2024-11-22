from django.db import models

class User(models.Model):
    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.username

class Expense(models.Model):
    class CategoryChoices(models.IntegerChoices):
        OTHER = 0
        FOOD = 1
        TRAVEL = 2
        UTILITIES = 3
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    category = models.IntegerField(choices=CategoryChoices, default=0)

    def __str__(self):
        return f"{self.title} - {self.amount}"
