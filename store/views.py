from django.contrib.auth.models import User
from rest_framework import viewsets, permissions, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response

from store.models import *
from store.serializers import *


class CreateListRetrieveViewSet(mixins.CreateModelMixin,
                                mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                viewsets.GenericViewSet):
    """
    A viewset that provides `retrieve`, `create`, and `list` actions.
    """
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({"user": self.request.user})
        return context


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
        return CartItem.objects.filter(user=self.request.user, in_order=False)

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


class OrderViewSet(CreateListRetrieveViewSet):
    """
    Create, list, and retrieve orders. Per-order actions available.
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by("-id")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=["POST"])
    def confirm(self, request, pk=None):
        order = self.get_object()
        if order.status != "Created":
            return Response({"error": "Order cannot be confirmed in this state."}, status=status.HTTP_400_BAD_REQUEST)
        order.status = "Confirmed"
        order.save()
        return Response(OrderSerializer(data=order).data)