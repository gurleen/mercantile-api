from django.db import models
from django.contrib.auth.models import User

from address.models import AddressField
from djmoney.models.fields import MoneyField


class Product(models.Model):
    name = models.CharField(max_length=50)
    brand = models.CharField(max_length=30)
    description = models.TextField()
    quantity = models.IntegerField()
    price = MoneyField(max_digits=6, decimal_places=2, default_currency="USD")


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="img/")


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField()


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = AddressField()
    items = models.ManyToManyField(CartItem)
