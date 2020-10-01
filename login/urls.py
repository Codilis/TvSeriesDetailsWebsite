from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.loginuser, name='loginuser'),
    path('', views.loginuser, name='loginuser'),
    path('forgetpassword/', views.forgetpassword, name='forgetpassword'),
    path('changepassword/', views.changepassword, name='changepassword'),
    path('createaccount/', views.createaccount, name='createaccount'),
    path('logincheck/', views.logincheck, name='logincheck'),
    path('logout/', views.userlogout, name='userlogout'),
]
