# Generated by Django 2.0.3 on 2020-05-03 06:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0007_extra'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Salads',
            new_name='Salad',
        ),
        migrations.RenameModel(
            old_name='Subs',
            new_name='Sub',
        ),
        migrations.RenameModel(
            old_name='Toppings',
            new_name='Topping',
        ),
    ]