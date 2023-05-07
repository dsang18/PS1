from django.db import models
from django.contrib.auth.hashers import make_password

class Customer(models.Model):
    id = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address = models.TextField(max_length=500)

    def save(self):
        self.password = make_password(self.password)
        super(Customer, self).save()

    def __str__(self):
        return self.fullname
    

class Farmer(models.Model):
    id = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)


    def save(self):
        self.password = make_password(self.password)
        super(Farmer, self).save()

    def __str__(self):
        return self.fullname
    


class FoodGrains(models.Model):
    farmer = models.ForeignKey(Farmer, db_column='farmer', on_delete=models.CASCADE)
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    image = models.ImageField(upload_to='images/')
    
    def __str__(self):
        return self.name
    

class cart(models.Model):
    customer = models.ForeignKey(Customer, db_column='customer', on_delete=models.CASCADE)
    FoodGrains = models.ForeignKey(FoodGrains, db_column='in_cart_item', on_delete=models.CASCADE)
    quantity = models.IntegerField()
