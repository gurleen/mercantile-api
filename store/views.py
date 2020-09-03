from django.contrib.auth.models import User
from rest_framework import viewsets, permissions

from store.models import *
from store.serializers import *

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """
    List and filter all available products.
    """
    queryset = Product.objects.all().order_by('-date_added')
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

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)
    