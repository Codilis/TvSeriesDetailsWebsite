from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect, HttpResponseNotFound
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from .models import LoginForm, CreateAccountForm, ChangePasswordForm, ForgetPasswordForm, ResetPasswordForm
from django.conf import settings
from django.urls import reverse_lazy
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
	if request.method == 'POST':
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Request"
					email_template_name = "forgetpassword/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'tv-series-details.herokuapp.com',
					'site_name': 'Tv Series Details',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email,  settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect("forgetpasswordmessage")
	login_page = loader.get_template('forgetpassword/forgetpassword.htm')
	context = {}
	context['password_reset_form'] = ForgetPasswordForm()
	return HttpResponse(login_page.render(context, request))


def forgetpasswordmessage(request):
	if request.user.is_authenticated:
		return HttpResponseRedirect('/main/')
	forget_password_page = loader.get_template('forgetpassword/forgetpassword.htm')
	success_message = ["We've emailed you instructions for setting your password, if an account exists with the email you entered. You should receive them shortly.",
						"If you don't receive an email, please make sure you've entered the address you registered with, and check your spam folder."]
	context = {"success_message":success_message, "hide_form":'Y'}
	return HttpResponse(forget_password_page.render(context, request))

def forgetpasswordreset(request, uidb64, token):
	context = {}
	context['password_reset_form'] = ResetPasswordForm(request.user)
	if request.method == 'POST':
		user = User.objects.get(pk=urlsafe_base64_decode(uidb64))
		form = SetPasswordForm(request.user, request.POST)
		if form.is_valid():
			form.user = user
			form.save()
			messages.success(request, 'Your password was successfully updated! Login to continue')
			email_template_name = "forgetpassword/password_reset_confirmation.txt"
			subject = "Password Reset Completed"
			c = {
			"user_email":user.email,
			"user":user.get_full_name()
			}
			email = render_to_string(email_template_name, c)
			send_mail(subject, email,  settings.EMAIL_HOST_USER, [user.email])
			return HttpResponseRedirect('/login/')
		else:
			for msg in form.error_messages:
				if 'inactive' not in form.error_messages[msg]:
					messages.error(request, f"{form.error_messages[msg]}")

	login_page = loader.get_template('forgetpassword/forgetpassword.htm')
	context["hide_form"] = 'N'
	user = User.objects.get(pk=urlsafe_base64_decode(uidb64))
	if default_token_generator.check_token(user=user, token=token):
		return HttpResponse(login_page.render(context, request))
	return HttpResponseNotFound()


# Change Password
@login_required(login_url='/login/')
def changepassword(request):
	if not request.user.is_authenticated:
		HttpResponseRedirect('/login/')
	context = {}
	context['username'] = request.user.get_full_name()
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
