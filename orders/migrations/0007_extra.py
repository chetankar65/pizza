# Generated by Django 2.0.3 on 2020-05-03 04:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0006_dinnerplatter_pasta_salads_subs'),
    ]

    operations = [
        migrations.CreateModel(
            name='Extra',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
    ]
