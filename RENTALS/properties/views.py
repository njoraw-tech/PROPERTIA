from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse

app_name = 'properties'

from django.shortcuts import render, redirect
from .models import Property
from .forms import PropertyForm



def property_list(request):
    if request.method == "POST":
        form = PropertyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('properties:property_list')
    
    properties = Property.objects.all()
    form = PropertyForm()
    return render(request, 'properties/propertyIndex.html', {
        'properties': properties,
        'form': form
    })