from django import forms
from .models import Payment

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['property', 'tenant', 'amount', 'description', 'date']
        widgets = {
            'property': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Select Property'}),
            'tenant': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Select Tenant'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Amount'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }