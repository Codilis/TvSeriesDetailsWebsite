from django.db import models
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import password_validation
from django import forms
from django.contrib.auth.models import User

# Create your models here.
class LoginForm(AuthenticationForm):
	def __init__(self, *args, **kwargs):
		super(LoginForm, self).__init__(*args, **kwargs)
	username = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'Email', 'class': 'login-username'}), label='')
	password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'login-password'}), label='')

# source: https://stackoverflow.com/questions/48049498/django-usercreationform-custom-fields
class CreateAccountForm(UserCreationForm):
	email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email', 'class': 'login-username'}), label='')
	fullname = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Full Name', 'class': 'login-username'}), label = "")
	password1 = forms.CharField(label=_(''), widget=(forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'login-password'})))#, help_text=password_validation.password_validators_help_text_html())
	password2 = forms.CharField(label=_(''), widget=forms.PasswordInput(attrs={'placeholder': 'Confirm Password', 'class': 'login-password'}), help_text=_(''))

	class Meta:
		model = User
		fields = ("fullname", "email")

	def save(self, commit=True):
		user = super(CreateAccountForm, self).save(commit=False)
		name_part = self.cleaned_data["fullname"].split()
		if len(name_part) <= 1:
			first_name, last_name = self.cleaned_data["fullname"], ''
		else:
			first_name, last_name = " ".join(name_part[:-1]), name_part[-1]
		user.first_name = first_name
		user.last_name = last_name
		user.username = self.cleaned_data["email"]
		user.email = self.cleaned_data["email"]
		if commit:
			user.save()
		return user
