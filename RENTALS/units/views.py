from django.shortcuts import render, redirect

# Create your views here.


from .models import Unit
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
            return redirect('units:unit_list')
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
    })