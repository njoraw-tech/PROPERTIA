from django.shortcuts import render
from django.views import View

# Create your views here.
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello! This is the Accounts page.")