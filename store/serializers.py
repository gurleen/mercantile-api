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
        read_only_fields = ["id", "subtotal"]

    def create(self, validated_data):
        print(validated_data)
        validated_data.update({
            "user": self.context.get("user")
        })
        existing = CartItem.objects.filter(
            product=validated_data["product"], user=validated_data["user"]
        ).first()
        if existing is not None:
            existing.amount += validated_data["amount"]
            existing.save()
            return existing
        return CartItem.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.amount = validated_data.get("amount")
        if instance.amount == 0:
            instance.delete()
        else:
            instance.save()
        return instance


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["address", "city", "state"]