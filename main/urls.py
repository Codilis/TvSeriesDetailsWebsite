from django.urls import path

from . import views

urlpatterns = [
    path('main/', views.home_view, name='home_view'),
]
