# Generated by Django 4.2.1 on 2023-05-07 18:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('farmers_app', '0005_delete_cart_delete_foodgrains'),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodGrains',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('quantity', models.IntegerField()),
                ('image', models.ImageField(upload_to='images/')),
                ('farmer', models.ForeignKey(db_column='farmer', on_delete=django.db.models.deletion.CASCADE, to='farmers_app.farmer')),
            ],
        ),
        migrations.CreateModel(
            name='cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField()),
                ('FoodGrains', models.ForeignKey(db_column='in_cart_item', on_delete=django.db.models.deletion.CASCADE, to='farmers_app.foodgrains')),
                ('customer', models.ForeignKey(db_column='customer', on_delete=django.db.models.deletion.CASCADE, to='farmers_app.farmer')),
            ],
        ),
    ]
