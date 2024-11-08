# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('hugging.html/', views.use_hugging_face, name='use_hugging_face'),
]
