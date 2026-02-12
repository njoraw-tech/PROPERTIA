from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST

# Create your views here.


from .models import Unit
from tenants.models import Tenant
from properties.models import Property
from django import forms

class UnitForm(forms.ModelForm):
    class Meta:
        model = Unit
        fields = ['property', 'name', 'rent_amount', 'description']
        widgets = {
            'property': forms.Select(attrs={'class': 'form-select'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. House 712'}),
            'rent_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

def units_list(request):
    # 1. Handle POST (Form Submission)
    if request.method == "POST":
        form = UnitForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('units:units_list')
        # If form is NOT valid, we don't reset it; we let it pass 
        # to the template so the user can see the error messages.
    else:
        # 2. Handle GET (Initial Page Load)
        form = UnitForm()

    # 3. Filtering Logic (Common to both or just GET)
    units = Unit.objects.all()
    property_filter = request.GET.get('property')
    status_filter = request.GET.get('status')
    
    if property_filter:
        units = units.filter(property_id=property_filter)
    if status_filter:
        units = units.filter(status=status_filter)
            
    # 4. Return the Response
    return render(request, 'units/units_view.html', {
        'units': units,
        'form': form, # This is now guaranteed to exist!
        'properties': Property.objects.all(),
        'tenants': Tenant.objects.filter(unit__isnull=True),
    })


def assign_tenant(request, pk):
    """Assign a tenant to a unit"""
    unit = get_object_or_404(Unit, pk=pk)
    
    if request.method == 'POST':
        tenant_id = request.POST.get('tenant_id')
        
        if tenant_id:
            try:
                tenant = Tenant.objects.get(id=tenant_id)
                unit.tenant_name = f"{tenant.first_name} {tenant.last_name}"
                unit.status = 'occupied'
                unit.save()
                
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': True, 'message': f'Tenant {tenant.first_name} {tenant.last_name} assigned to {unit.name}'})
                else:
                    return redirect('units:units_list')
            except Tenant.DoesNotExist:
                return JsonResponse({'success': False, 'message': 'Tenant not found'}, status=400)
        else:
            return JsonResponse({'success': False, 'message': 'Please select a tenant'}, status=400)
    
    # Return available tenants for modal
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        tenants = Tenant.objects.filter(unit__isnull=True)
        return JsonResponse({
            'unit_id': unit.id,
            'unit_name': unit.name,
            'tenants': list(tenants.values('id', 'first_name', 'last_name'))
        })


def detach_tenant(request, pk):
    """Detach tenant from a unit"""
    unit = get_object_or_404(Unit, pk=pk)
    
    if request.method == 'POST':
        unit.tenant_name = None
        unit.status = 'vacant'
        unit.save()
        
        return JsonResponse({'success': True, 'message': f'Tenant detached from {unit.name}'})


@require_POST
def delete_units(request):
    """Delete selected units"""
    unit_ids = request.POST.getlist('unit_ids[]')
    
    if unit_ids:
        Unit.objects.filter(id__in=unit_ids).delete()
        return JsonResponse({'success': True, 'message': f'{len(unit_ids)} unit/s deleted successfully'})
    
    return JsonResponse({'success': False, 'message': 'No units selected'})