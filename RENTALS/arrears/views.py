from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse

from properties.models import Property
from units.models import Unit
from tenants.models import Tenant
from invoices.models import Invoice  # Assuming you have an Invoice model
from payments.models import Payment
from django.db.models import Sum

def arrears_report(request):
    # 1. Get filter parameters
    prop_id = request.GET.get('property')
    unit_id = request.GET.get('unit')
    tenant_id = request.GET.get('tenant')

    # 2. Base Query: Start with active tenants
    tenants = Tenant.objects.all()

    # 3. Apply Filters
    if prop_id:
        tenants = tenants.filter(unit__property_id=prop_id)
    if unit_id:
        tenants = tenants.filter(unit_id=unit_id)
    if tenant_id:
        tenants = tenants.filter(id=tenant_id)

    # 4. Calculate Arrears Data
    report_data = []
    for tenant in tenants:
        total_invoiced = Invoice.objects.filter(tenant=tenant).aggregate(Sum('amount'))['amount__sum'] or 0
        total_paid = Payment.objects.filter(tenant=tenant).aggregate(Sum('amount'))['amount__sum'] or 0
        total_payment_balance = Payment.objects.filter(tenant=tenant).aggregate(Sum('balance'))['balance__sum'] or 0
        balance = total_invoiced - total_paid

        # Only show in report if there is a balance (Arrears)
        if balance > 0:
            # Get the latest invoice for display details
            latest_inv = Invoice.objects.filter(tenant=tenant).last()
            
            report_data.append({
                'tenant': tenant,
                'invoice_no': latest_inv.invoice_number if latest_inv else "N/A",
                'invoice_type': "Rent",
                'invoice_amount': total_invoiced,
                'total_paid': total_paid,
                'balance': balance,
                'payment_remaining': total_payment_balance,
                'due_date': latest_inv.due_date if latest_inv else "N/A",
            })

    return render(request, 'arrears/arrears_view.html', {
        'report_data': report_data,
        'properties': Property.objects.all(),
        'units': Unit.objects.all(),
        'tenants': Tenant.objects.all(),
    })