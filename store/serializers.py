from store.models import *
from rest_framework import serializers
from djmoney.contrib.django_rest_framework import MoneyField
from djmoney.money import Money


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["name", "image"]


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "brand", "description", "price", "first_image"]


class CartItemSerializer(serializers.ModelSerializer):
    item_total = MoneyField(max_digits=8, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = ["id", "product", "amount", "item_total"]
        read_only_fields = ["id", "item_total"]

    def create(self, validated_data):
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
        fields = ["id", "address", "city", "state"]


class OrderSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    subtotal = serializers.SerializerMethodField()
    class Meta:
        model = Order
        fields = ["id", "status", "address", "items", "subtotal"]
        read_only_fields = ["items", "status"]

    def create(self, validated_data):
        instance = Order.objects.create(**validated_data)
        cart = CartItem.objects.filter(user=self.context.get("user"))
        cart.update(in_order=True)
        [instance.items.add(item) for item in cart]
        instance.status = "Created"
        instance.save()
        return instance

    def get_subtotal(self, order):
        subtotal = Money(0, "USD")
        for item in order.items.all():
            subtotal += (item.product.price * item.amount)
        return str(subtotal)