from django.shortcuts import render
from django.views.generic import TemplateView

from store.models import *


class HomePageView(TemplateView):

    template_name = "store/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["latest_products"] = Product.objects.order_by("-id")[:3][::-1]
        return context