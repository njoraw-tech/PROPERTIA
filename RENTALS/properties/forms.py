from django import forms
from .models import Property

class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        fields = ['name', 'address', 'county', 'total_units', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'e.g. Riverside Apartments'}),
            'address': forms.TextInput(attrs={'placeholder': '123 Street, City'}),
            'county': forms.TextInput(attrs={'placeholder': 'Select County'}),
            'total_units': forms.NumberInput(attrs={'placeholder': '0'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Optional details...'}),
        }
