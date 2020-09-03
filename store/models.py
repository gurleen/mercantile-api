from django.db import models
from django.contrib.auth.models import User

from address.models import AddressField
from djmoney.models.fields import MoneyField


class ProductImage(models.Model):
    name = models.CharField(max_length=30)
    image = models.ImageField(upload_to="img/")

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=50)
    brand = models.CharField(max_length=30)
    description = models.TextField()
    quantity = models.IntegerField()
    price = MoneyField(max_digits=6, decimal_places=2, default_currency="USD")
    date_added = models.DateField(auto_now_add=True)
    images = models.ManyToManyField(ProductImage)

    def __str__(self):
        return f"{self.brand} {self.name} - {self.price} ({self.quantity})"

    @property
    def first_image(self):
        return self.images.first().image.url


class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    amount = models.IntegerField()

    def __str__(self):
        return f"{self.amount}x {self.product.name} - {self.user}"

    def subtotal(self):
        return self.product.price * self.amount


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address = AddressField()
    items = models.ManyToManyField(CartItem)
    status = models.CharField(max_length=15)
