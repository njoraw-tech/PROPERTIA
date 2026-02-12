from django import forms
from .models import Tenant
from properties.models import Property

class TenantForm(forms.ModelForm):
    # Add a property field that's not in the model
    property = forms.ModelChoiceField(
        queryset=Property.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Property',
        required=True
    )
    
    class Meta:
        model = Tenant
        fields = ['first_name', 'last_name', 'phone_number', 'next_of_kin_name', 'description', 'deposit_required', 'deposit_amount', 'next_of_kin_phone_number']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'next_of_kin_name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'deposit_required': forms.CheckboxInput(attrs={'class': 'form-check-input', 'id': 'depositCheck'}),
            'deposit_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter deposit amount'}),
            'next_of_kin_phone_number': forms.TextInput(attrs={'class': 'form-control'}),
        }