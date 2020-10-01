from django.shortcuts import render
from .models import UserTvSeries, UserTvSeriesModel
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.contrib import messages
from .constants import AVAILABLE_CHOICES_KEYS

# Create your views here.
@login_required(login_url='/login/')
def home_view(request):
	if not request.user.is_authenticated:
		HttpResponseRedirect('/login/')
	main_page = loader.get_template("main.htm")
	context = {}
	context['username'] = request.user
	if request.method == 'POST':
		form = UserTvSeries(request.POST)
		if form.is_valid():
			tv_series_id = form.cleaned_data.get('tv_series_id')
			p = form.save(commit=False)
			print(request.user)
			p.user = request.user
			p.save()
			context['form'] = form
			messages.error(request, f"Successfully Added New Series: {tv_series_id}")
		else:
			for field, items in form.errors.items():
				for item in items:
					messages.error(request, '{}: {}'.format(field, item))
			context['form'] = form
	else:
		context['form'] = UserTvSeries()
	return HttpResponse(main_page.render(context, request))

@login_required(login_url='/login/')
def view_subscription(request):
	if not request.user.is_authenticated:
		HttpResponseRedirect('/login/')
	main_page = loader.get_template("view_subscription.htm")
	details = UserTvSeriesModel.objects.filter(user=request.user)
	context = {}
	context['username'] = request.user
	context['subscribed_series'] = details
	context['series_update_keys'] = AVAILABLE_CHOICES_KEYS
	return HttpResponse(main_page.render(context, request))
