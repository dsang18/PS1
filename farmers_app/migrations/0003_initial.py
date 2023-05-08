# Generated by Django 4.2.1 on 2023-05-07 17:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('farmers_app', '0002_remove_foodgrains_farmer_delete_cart_delete_customer_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='FoodGrains',
            fields=[
                ('farmer_mail', models.CharField(max_length=100)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('quantity', models.IntegerField()),
                ('image', models.ImageField(upload_to='images/')),
            ],
        ),
        migrations.CreateModel(
            name='cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('customer_mail', models.CharField(max_length=100)),
                ('quantity', models.IntegerField()),
                ('FoodGrains', models.ForeignKey(db_column='in_cart_item', on_delete=django.db.models.deletion.CASCADE, to='farmers_app.foodgrains')),
            ],
        ),
    ]