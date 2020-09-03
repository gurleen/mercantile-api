from django.urls import path, include
from rest_framework import routers
from store import views


router = routers.DefaultRouter()
router.register(r"product", views.ProductViewSet)
router.register(r"images", views.ProductImageViewSet)
router.register(r"cart", views.CartItemViewSet, basename="cart")

urlpatterns = [
    path("", include(router.urls)),
    path("auth/", include("rest_framework.urls", namespace="rest_framework")),
]
