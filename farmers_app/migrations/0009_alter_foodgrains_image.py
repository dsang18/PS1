# Generated by Django 4.2.1 on 2023-05-08 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('farmers_app', '0008_alter_foodgrains_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='foodgrains',
            name='image',
            field=models.ImageField(upload_to='images/'),
        ),
    ]
