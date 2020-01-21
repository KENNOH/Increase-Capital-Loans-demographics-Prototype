from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver


class Unit_station_names(models.Model):
    station_name = models.CharField(max_length=255)
    daily_target = models.IntegerField()
    monthly_target = models.IntegerField()

    def __str__(self):
        return self.station_name

class Loan_status(models.Model):
    loan_status = models.CharField(max_length=255)

    def __str__(self):
        return self.loan_status

class Loans(models.Model):
    customer_id = models.CharField(max_length=255)
    customer_station = models.ForeignKey(Unit_station_names,null=True,on_delete=models.SET_NULL)
    loan_status = models.ForeignKey(Loan_status, null=True, on_delete=models.SET_NULL)
    loan_amount = models.IntegerField()
    loan_code = models.CharField(max_length=255)
    loan_date = models.DateField(blank=True, null=True)
    due_date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.loan_code


class Customers(models.Model):
    MAYBECHOICE = (
        ('1', 'Never borrowed'),
        ('2', 'Current Loan'),
        ('3', 'Repaid'),
        ('4', 'Suspended'),
        ('5', 'Blacklisted'),
    )
    CHOICE = (
        ('1','Female'),
        ('2', 'Male'),
    )
    name = models.CharField(max_length=255, verbose_name='Full Name:')
    phone = models.CharField(max_length=12, verbose_name='Mobile Reference', unique=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    customer_id = models.CharField(max_length=255)
    created_at = models.DateField(max_length=255)
    loan_status = models.CharField(max_length=3, choices=MAYBECHOICE, default=2)
    gender = models.CharField(max_length=3, choices=CHOICE, default=1)

    class Meta:
        verbose_name_plural = 'Customers'

    def __str__(self):
        return self.name
    


class Repayments(models.Model):
    name = models.CharField(max_length=255, default="Full name")
    phone = models.CharField(max_length=12, verbose_name='Mobile Reference', unique=True)
    loan_code = models.ForeignKey(Loans, null=True, on_delete=models.SET_NULL)
    repayment_date = models.DateField(max_length=255)
    amount_paid = models.IntegerField()

    class Meta:
        verbose_name_plural = 'Repayments'

    def __str__(self):
        return self.name



