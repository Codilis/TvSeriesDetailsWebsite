from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import LoginForm, CreateAccountForm, ChangePasswordForm
from main.models import UserTvSeries


# Create your views here.
# Login View
def loginuser(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect('/main/')
	login_page = loader.get_template('login/login.htm')
	context = {}
	context['form'] = LoginForm()
	return HttpResponse(login_page.render(context, request))

# Create Account
def createaccount(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect('/main/')
	login_page = loader.get_template('login/createaccount.htm')
	context = {}
	if request.method == 'POST':
		form = CreateAccountForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('email')
			p = form.save()
			password = form.cleaned_data.get('password1')
			messages.success(request, f"New account created: {username}")
			user = authenticate(username=username, password=password)
			login(request, user)
			return HttpResponseRedirect('/main/')
		else:
			for msg in form.error_messages:
				if 'inactive' not in form.error_messages[msg]:
					messages.error(request, f"{form.error_messages[msg]}")
			context['form'] = form
			return render(request = request, template_name = "login/createaccount.htm", context={"form":form})
	else:
		context['form'] = CreateAccountForm()
	return HttpResponse(login_page.render(context, request))

# Forget Password
def forgetpassword(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect('/main/')
	login_page = loader.get_template('login/forgetpassword.htm')
	context = {}
	return HttpResponse(login_page.render(context, request))

# Change Password
@login_required(login_url='/login/')
def changepassword(request):
	if not request.user.is_authenticated:
		HttpResponseRedirect('/login/')
	context = {}
	context['username'] = request.user
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save()
			username = request.user
			password = form.cleaned_data.get('new_password2')
			update_session_auth_hash(request, user)  # Important!
			messages.success(request, 'Your password was successfully updated!')
			user = authenticate(username=username, password=password)
			login(request, user)
			return HttpResponseRedirect('/changepassword/')
		else:
			for msg in form.error_messages:
				if 'inactive' not in form.error_messages[msg]:
					messages.error(request, f"{form.error_messages[msg]}")
			context['form'] = ChangePasswordForm(request.user)
	else:
			context['form'] = ChangePasswordForm(request.user)
	login_page = loader.get_template('login/changepassword.htm')
	return HttpResponse(login_page.render(context, request))

# Check Credentials
def logincheck(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect('/main/')
	form = LoginForm(request=request, data=request.POST)
	context = {}
	if request.method != 'POST':
		return HttpResponseForbidden()

	if not form.is_valid():
		for msg in form.error_messages:
			if 'inactive' not in form.error_messages[msg]:
				messages.error(request, f"{form.error_messages[msg]}")
		context['form'] = form
		return render(request = request, template_name = "login/login.htm", context={"form":form})

	username = form.cleaned_data.get('username')
	password = form.cleaned_data.get('password')
	user = authenticate(username=username, password=password)
	if user is None:
		for msg in form.error_messages:
			if 'inactive' not in form.error_messages[msg]:
				messages.error(request, f"{form.error_messages[msg]}")
		context['form'] = form
		return render(request = request, template_name = "login/login.htm", context={"form":form})

	if user.is_active:
		login(request, user)
		return HttpResponseRedirect('/main/')

	for msg in form.error_messages:
		if 'inactive' not in form.error_messages[msg]:
			messages.error(request, f"{form.error_messages[msg]}")
	context['form'] = form
	return render(request = request, template_name = "login/login.htm", context={"form":form})


def userlogout(request):
	if request.user.is_authenticated:
		logout(request)
	return HttpResponseRedirect('/login/')
