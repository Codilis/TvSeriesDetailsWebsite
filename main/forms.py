from .constants import AVAILABLE_CHOICES
from datetime import datetime
from django import forms

class UserTvSeries(forms.Forms):
	tv_series_id = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'IMDb ID', 'class': 'series-name'}), label='')
	update_type = forms.TypedChoiceField(choices=AVAILABLE_CHOICES, widget=forms.Select(attrs={'class': 'series-update-type'}), label='')
	date_added = forms.DateTimeField(initial=datetime.now, widget=forms.DateTimeInput(attrs={'hidden': 'hidden'}), label='')
