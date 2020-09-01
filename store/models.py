from django.db import models


class Product(models.Model):
    name = models.TextField(max_length=50)
    brand = models.TextField(max_length=30)
    description = models.TextField(max_length=500)
    quantity = models.IntegerField()
    price = models.IntegerField()


class ProductImage(models.Model):
    product = models.ForeignField(Product, default=None)
    image = models.ImageField(upload_to="img/")


class CartItem(models.Model):
    product = models.ForeignField(Product, default=None)
    amount = models.IntegerField()
