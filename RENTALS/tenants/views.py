from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q

from django.views.decorators.http import require_POST
from .models import Tenant
from .forms import TenantForm
from django.http import JsonResponse
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
        # Filter by property: show tenants with units in that property, or tenants with no unit assigned
        tenants = tenants.filter(Q(unit__property_id=property_filter) | Q(unit__isnull=True))
    
    if status_filter:
        tenants = tenants.filter(status=status_filter)

    return render(request, 'tenants/tenants_view.html', {
        'tenants': tenants,
        'form': form,
        'properties': Property.objects.all(),
        'selected_property': property_filter,
        'selected_status': status_filter,
    })

@require_POST
def delete_tenants(request):
    tenant_ids = request.POST.getlist('tenant_ids[]')
    try:
        # This deletes the tenants. If you have OnDelete=SET_NULL on Units, 
        # the units will automatically become vacant.
        Tenant.objects.filter(id__in=tenant_ids).delete()
        return JsonResponse({'success': True, 'message': f'Successfully deleted {len(tenant_ids)} tenants.'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})