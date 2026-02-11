from django.shortcuts import render
from django.views import View


# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'dashboard/dashboard.html', {})