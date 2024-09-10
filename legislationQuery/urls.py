from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("documentation", views.documentation, name="documentation"),
    path("open_ai_connect", views.open_ai_connect, name="open_ai_connect"),
]