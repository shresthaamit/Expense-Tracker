from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

class Income(models.Model):
    PROFESSION_CHOICES= [
        ('doctor', 'Doctor'),
        ('engineer', 'Engineer'),
        ('teacher', 'Teacher'),
    ]
    CATEGORY_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense')
    ] 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profession = models.CharField(max_length=100, choices=PROFESSION_CHOICES)
    source_1_name = models.CharField(max_length=100, blank=True)
    source_1_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    source_2_name = models.CharField(max_length=100, blank=True)
    source_2_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    source_3_name = models.CharField(max_length=100, blank=True)
    source_3_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='income')
    def __str__(self):
        return self.user.username
    verbose_name = "Income"
    verbose_name_plural = "Income"

class Expenses(models.Model):
    CATEGORY_CHOICES = [
        ('income', 'Income'),
        ('expense', 'Expense')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    source_1_name = models.CharField(max_length=100, blank=True)
    source_1_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    source_2_name = models.CharField(max_length=100, blank=True)
    source_2_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    source_3_name = models.CharField(max_length=100, blank=True)
    source_3_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    date = models.DateField(auto_now_add=True)
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='expense')
    def __str__(self):
            return self.user.username
    class Meta:
       
        verbose_name = "Expense"
        verbose_name_plural = "Expenses"