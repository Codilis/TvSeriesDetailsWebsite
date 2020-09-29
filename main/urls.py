from django.urls import path

from . import views

urlpatterns = [
    path('main/', views.home_view, name='home_view'),
    path('viewsubscription/', views.view_subscription, name='view_subscription'),
]
