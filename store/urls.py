from django.urls import path

from store.views import HomePageView

urlpatterns = [
    path("", HomePageView.as_view(), name="home")
]
