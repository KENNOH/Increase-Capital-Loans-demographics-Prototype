# Generated by Django 2.2 on 2019-12-09 09:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_auto_20191209_1217'),
    ]

    operations = [
        migrations.AlterField(
            model_name='repayments',
            name='loan_code',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.Loans'),
        ),
        migrations.AlterField(
            model_name='repayments',
            name='name',
            field=models.CharField(default='Full name', max_length=255),
        ),
    ]
