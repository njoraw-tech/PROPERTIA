from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse


from .models import Tenant
from .forms import TenantForm
from properties.models import Property

def tenant_list(request):
    if request.method == "POST":
        form = TenantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('tenants:tenant_list')
    else:
        form = TenantForm()

    # Filtering
    tenants = Tenant.objects.all()
    property_filter = request.GET.get('property')
    status_filter = request.GET.get('status')

    if property_filter:
        tenants = tenants.filter(unit__property_id=property_filter)
    if status_filter:
        tenants = tenants.filter(status=status_filter)

    return render(request, 'tenants/tenants_view.html', {
        'tenants': tenants,
        'form': form,
        'properties': Property.objects.all(),
    })