from django.urls import path, include   
from django.conf.urls import url
from rest_framework import routers
from rest_framework.authtoken import views as auth_views

from store import views


router = routers.DefaultRouter()
router.register(r"product", views.ProductViewSet)
router.register(r"images", views.ProductImageViewSet)
router.register(r"cart", views.CartItemViewSet, basename="cart")
router.register(r"address", views.AddressViewSet, basename="address")

urlpatterns = [
    path("", include(router.urls)),
    url(r'^api-token-auth/', auth_views.obtain_auth_token)
]
