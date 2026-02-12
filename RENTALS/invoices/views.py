from django.shortcuts import render, redirect

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse

from .models import Invoice
from properties.models import Property
from units.models import Unit

def invoice_list(request):
    # Handle Bulk Generation
    if request.method == "POST" and 'bulk_generate' in request.POST:
        prop_id = request.POST.get('property')
        due_date = request.POST.get('due_date')
        inv_type = request.POST.get('type')
        
        # Get all units for this property that have active tenants
        units = Unit.objects.filter(property_id=prop_id, status='occupied')
        for u in units:
            tenant = u.tenants.filter(status='active').first()
            if tenant:
                Invoice.objects.create(
                    unit=u,
                    tenant=tenant,
                    amount=u.rent_amount,
                    type=inv_type,
                    due_date=due_date
                )
        return redirect('invoices:invoice_list')

    invoices = Invoice.objects.all().order_by('-due_date')
    return render(request, 'invoices/invoices_view.html', {
        'invoices': invoices,
        'properties': Property.objects.all(),
        'units': Unit.objects.all(),
    })