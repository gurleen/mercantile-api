from store.models import *
from rest_framework import serializers
from djmoney.contrib.django_rest_framework import MoneyField


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["name", "image"]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "brand", "description", "price", "first_image"]


class CartItemSerializer(serializers.ModelSerializer):
    subtotal = MoneyField(max_digits=8, decimal_places=2)

    class Meta:
        model = CartItem
        fields = ["id", "product", "amount", "subtotal"]
