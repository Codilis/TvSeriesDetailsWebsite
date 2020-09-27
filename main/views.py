from django.shortcuts import render
from .models import UserTvSeries

# Create your views here.
def home_view(request):
    context = {}
    context['form'] = UserTvSeries()
    return render( request, "main.htm", context)
