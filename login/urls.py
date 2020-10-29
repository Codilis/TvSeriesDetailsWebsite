from django.urls import path, include, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('login/', views.loginuser, name='loginuser'),
    path('', views.loginuser, name='loginuser'),
    path('forgetpassword/',  views.forgetpassword,  name='forgetpassword'),
    path('changepassword/', views.changepassword, name='changepassword'),
    path('createaccount/', views.createaccount, name='createaccount'),
    path('logincheck/', views.logincheck, name='logincheck'),
    path('logout/', views.userlogout, name='userlogout'),
	# Password RESET
    path('forgetpassword/done/', views.forgetpasswordmessage, name='forgetpasswordmessage'),
    path('reset/<uidb64>/<token>/', views.forgetpasswordreset, name='forgetpasswordreset'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='passwordresetcomplete'),

]
