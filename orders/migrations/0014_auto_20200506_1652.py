# Generated by Django 2.0.3 on 2020-05-06 16:52

import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0013_auto_20200506_1639'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='extras',
        ),
        migrations.AddField(
            model_name='cart',
            name='extras',
            field=models.CharField(default='1', max_length=20, validators=[django.core.validators.RegexValidator(re.compile('^\\d+(?:,\\d+)*\\Z'), code='invalid', message='Enter only digits separated by commas.')]),
        ),
    ]
