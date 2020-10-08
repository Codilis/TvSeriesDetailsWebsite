from django.shortcuts import render
from .models import UserTvSeries, UserTvSeriesModel, TvSeriesDetailsModel
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.contrib import messages
from .constants import AVAILABLE_CHOICES_KEYS
from django.views.decorators.csrf import csrf_exempt
from .imdb_functions import get_tv_series_name, get_series_latest_info, tv_series_email
from django.conf import settings
from django.core.mail import send_mail
from threading import Thread
from datetime import datetime, timedelta

# Create your views here.
@login_required(login_url='/login/')
def home_view(request):
	if not request.user.is_authenticated:
		HttpResponseRedirect('/login/')
	main_page = loader.get_template("main.htm")
	context = {}
	context['username'] = request.user.get_full_name()
	if request.method == 'POST':
		form = UserTvSeries(request.POST)
		if form.is_valid():
			tv_series_id = form.cleaned_data.get('tv_series_id')
			tv_seires_details = get_tv_series_name(tv_series_id)
			tv_series_name, tv_series_id = tv_seires_details
			tv_series_id = 'tt'+str(tv_series_id)
			if tv_series_name == 'CONNECTIONERROR':
				messages.error(request, f"Looks like we are having some issues, try again later.")
				return HttpResponseRedirect('/main/')
			if tv_series_name == 'NOTTVSERIES' or tv_series_name == 'NOTFOUNDSERIES':
				messages.error(request, f"{form.cleaned_data.get('tv_series_id')} Not a Valid Series Id")
				return HttpResponseRedirect('/main/')
			x = UserTvSeriesModel.objects.filter(user=request.user, tv_series_id=tv_series_id)
			if len(x) > 0:
				messages.error(request, f"Series {tv_series_id} Already Exist")
				return HttpResponseRedirect('/main/')
			p = form.save(commit=False)
			p.user = request.user
			p.tv_series_name = tv_series_name
			p.tv_series_id = tv_series_id
			p.last_email_sent = (datetime.utcnow()+timedelta(hours=5, minutes=30))
			p.date_added = (datetime.utcnow()+timedelta(hours=5, minutes=30))
			p.save()
			context['form'] = UserTvSeries()
			messages.success(request, f"Successfully Added New Series {tv_series_id}")
			# Send Email to user
			recipient_list = [request.user]
			tv_series_email(tv_series_id, tv_series_name, recipient_list)
			# Thread(target=tv_series_email, args=(tv_series_id, tv_series_name, recipient_list,)).start()
			return HttpResponseRedirect('/main/')
		else:
			for field, items in form.errors.items():
				for item in items:
					messages.error(request, '{}: {}'.format(field, item))
			context['form'] = form
	else:
		context['form'] = UserTvSeries()
	return HttpResponse(main_page.render(context, request))

@csrf_exempt
@login_required(login_url='/login/')
def view_subscription(request):
	if not request.user.is_authenticated:
		HttpResponseRedirect('/login/')
	context = {}
	context['username'] = request.user.get_full_name()
	context['series_update_keys'] = AVAILABLE_CHOICES_KEYS
	if request.method == 'POST':
		for key, value in request.POST.items():
			row = UserTvSeriesModel.objects.get(user=request.user, tv_series_id=key)
			row.update_type = value
			row.save()
		return HttpResponseRedirect('/viewsubscription/')
	main_page = loader.get_template("view_subscription.htm")
	context['subscribed_series'] = UserTvSeriesModel.objects.filter(user=request.user)
	for x in context['subscribed_series']:
		x.date_added = x.date_added.strftime("%B %d, %Y")
	return HttpResponse(main_page.render(context, request))

@csrf_exempt
@login_required(login_url='/login/')
def delete_subscriptions(request):
	if not request.user.is_authenticated:
		HttpResponseRedirect('/login/')
	context = {}
	context['username'] = request.user.get_full_name()
	context['series_update_keys'] = AVAILABLE_CHOICES_KEYS
	if request.method == 'POST':
		print(request.POST)
		for key, value in request.POST.items():
			UserTvSeriesModel.objects.filter(user=request.user, tv_series_id=value).delete()
	main_page = loader.get_template("view_subscription.htm")
	context['subscribed_series'] = UserTvSeriesModel.objects.filter(user=request.user)
	return HttpResponseRedirect('/viewsubscription/')
