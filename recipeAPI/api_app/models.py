from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, blank=True)
    def __str__(self):
        return self.username

class Recipe(models.Model):
    MEAL_TYPE_CHOICES = [
        ('B', 'Breakfast'),
        ('L', 'Lunch'),
        ('D', 'Dinner'),
    ]
    chef = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='recipes')
    title = models.CharField(max_length=255)
    description = models.TextField()
    meal_type = models.CharField(max_length=1, choices=MEAL_TYPE_CHOICES)
    ingredients = models.TextField(help_text="Comma-separated list of ingredients")
    image = models.ImageField(upload_to='recipes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title