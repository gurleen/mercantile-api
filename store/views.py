from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from rest_framework.permissions import IsAuthenticated

from store.models import *
from store.serializers import *


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List and filter all available products.
    """

    queryset = Product.objects.all().order_by("-date_added")
    serializer_class = ProductSerializer


class ProductImageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List and filter all available product images.
    """

    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer


class CartItemViewSet(viewsets.ModelViewSet):
    """
    CRUD for CartItems. Creating a cart item means that item is in your "cart".
    """

    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"user": self.request.user})
        return context


class AddressViewSet(viewsets.ModelViewSet):
    """
    CRUD for customer addresses.
    """

    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user).order_by("-id")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)