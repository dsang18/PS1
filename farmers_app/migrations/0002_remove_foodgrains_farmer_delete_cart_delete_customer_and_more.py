# Generated by Django 4.2.1 on 2023-05-07 17:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('farmers_app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='foodgrains',
            name='farmer',
        ),
        migrations.DeleteModel(
            name='cart',
        ),
        migrations.DeleteModel(
            name='Customer',
        ),
        migrations.DeleteModel(
            name='Farmer',
        ),
        migrations.DeleteModel(
            name='FoodGrains',
        ),
    ]
