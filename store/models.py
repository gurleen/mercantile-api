from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=50)
    brand = models.CharField(max_length=30)
    description = models.TextField()
    quantity = models.IntegerField()
    price = models.IntegerField()


class ProductImage(models.Model):
    product = models.ForeignField(Product, default=None)
    image = models.ImageField(upload_to="img/")


class CartItem(models.Model):
    product = models.ForeignKey(Product, default=None)
    amount = models.IntegerField()


class Address(models.Model):
    house_num = models.CharField(max_length=5)
    street = models.CharField(max_length=40)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=4)
    phone = models.CharField()


class Order(models.Model):
    user = models.ForeignKey(User, default=None)
    items = models.ManyToManyField(CartItem)
