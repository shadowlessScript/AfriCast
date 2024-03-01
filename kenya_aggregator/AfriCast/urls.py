from django.urls import path
from .views import index, business

urlpatterns = [
    path("", index, name="home"),
    path("category/<str:category>", business, name="category"),
]
