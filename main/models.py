from django.db import models
from .constants import AVAILABLE_CHOICES
from datetime import datetime
from django import forms
import random

# Create your models here.
class UserTvSeriesModel(models.Model):
	tv_series_id = models.CharField(max_length=1023)
	tv_series_name = models.CharField(max_length=1023, default='Not Added')
	update_type = models.CharField(max_length=1023)
	date_added = models.DateTimeField()
	user = models.CharField(max_length=1023)
	last_email_sent = models.DateTimeField(default=datetime.now)


class UserTvSeries(forms.ModelForm):
	tv_series_id = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'IMDb ID', 'class': 'series-name'}), label='')
	tv_series_name = forms.CharField(initial=datetime.now, widget=forms.TextInput(attrs={'hidden': 'hidden'}), label='')
	update_type = forms.TypedChoiceField(choices=AVAILABLE_CHOICES, widget=forms.Select(attrs={'class': 'series-update-type'}), label='')
	date_added = forms.DateTimeField(initial=datetime.now, widget=forms.DateTimeInput(attrs={'hidden': 'hidden'}), label='')
	last_email_sent = forms.DateTimeField(initial=datetime.now, widget=forms.DateTimeInput(attrs={'hidden': 'hidden'}), label='')
	user = forms.CharField(initial=datetime.now, widget=forms.TextInput(attrs={'hidden': 'hidden'}), label='')

	class Meta:
		model = UserTvSeriesModel
		fields = '__all__'


class TvSeriesDetailsModel(models.Model):
	tv_series_id = models.CharField(max_length=1023, unique=True)
	tv_series_name = models.CharField(max_length=1023)
	email_subject = models.TextField()
	email_body = models.TextField()

	def __str__(self):
		return self.tv_series_name
