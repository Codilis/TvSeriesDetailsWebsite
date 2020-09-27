from django.db import models
from .constants import AVAILABLE_CHOICES
from datetime import datetime
from django import forms
import random

# Create your models here.
class UserTvSeries(forms.Form):
	tv_series_name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'TV Series Name', 'class': 'form-control'}), label='')
	update_type = forms.TypedChoiceField(choices=AVAILABLE_CHOICES, label='')
	date_added = forms.DateField(initial=datetime.now, widget=forms.TextInput(attrs={'hidden': 'hidden'}), label='')
