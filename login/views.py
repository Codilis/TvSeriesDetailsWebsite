from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import LoginForm, CreateAccountForm


# Create your views here.
# Login View
def loginuser(request):
	login_page = loader.get_template('login/login.htm')
	context = {}
	context['form'] = LoginForm()
	return HttpResponse(login_page.render(context, request))

# Create Account
def createaccount(request):
	login_page = loader.get_template('login/createaccount.htm')
	context = {}
	if request.method == 'POST':
		form = CreateAccountForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('email')
			p = form.save()
			messages.success(request, f"New account created: {username}")
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
	login_page = loader.get_template('login/forgetpassword.htm')
	context = {}
	return HttpResponse(login_page.render(context, request))

# Change Password
def changepassword(request):
	login_page = loader.get_template('login/changepassword.htm')
	context = {}
	return HttpResponse(login_page.render(context, request))

# Check Credentials
def logincheck(request):
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
		# messages.success(request, f"Logged in Successfully")
		return HttpResponseRedirect('/main/')

	for msg in form.error_messages:
		if 'inactive' not in form.error_messages[msg]:
			messages.error(request, f"{form.error_messages[msg]}")
	context['form'] = form
	return render(request = request, template_name = "login/login.htm", context={"form":form})
