# Generated by Django 2.2 on 2019-12-08 09:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0009_loans'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Full Name:')),
                ('phone', models.CharField(max_length=12, unique=True, verbose_name='Mobile Reference')),
                ('email', models.EmailField(blank=True, max_length=255, null=True)),
                ('customer_id', models.CharField(max_length=255)),
                ('created_at', models.DateField(max_length=255)),
                ('loan_status', models.CharField(choices=[('1', 'Never borrowed'), ('2', 'Current Loan'), ('3', 'Repaid'), ('4', 'Suspended'), ('5', 'Blacklisted')], default=0, max_length=3)),
            ],
        ),
        migrations.CreateModel(
            name='Repayments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=12, unique=True, verbose_name='Mobile Reference')),
                ('repayment_date', models.DateField(max_length=255)),
                ('Amount_paid', models.IntegerField()),
                ('loan_code', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.Loans')),
                ('name', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
