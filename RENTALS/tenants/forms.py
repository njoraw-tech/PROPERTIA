from django import forms
from .models import Tenant
from units.models import Unit

class TenantForm(forms.ModelForm):
    # Add a unit field 
    unit = forms.ModelChoiceField(
        queryset=Unit.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Unit',
        required=False
    )
    
    class Meta:
        model = Tenant
        fields = ['first_name', 'last_name', 'phone_number', 'unit', 'next_of_kin_name', 'next_of_kin_phone_number', 'description', 'status', 'deposit_required', 'deposit_amount']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter phone number'}),
            'next_of_kin_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter next of kin name'}),
            'next_of_kin_phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter next of kin phone'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter description'}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'deposit_required': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'deposit_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter deposit amount'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['status'].required = False