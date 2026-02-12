from django.db import models

# Create your models here.
from properties.models import Property # Import the Property model

class Unit(models.Model):
    STATUS_CHOICES = [
        ('occupied', 'Occupied'),
        ('vacant', 'Vacant'),
    ]

    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='units')
    name = models.CharField(max_length=100)
    rent_amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='vacant')
    tenant_name = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.property.name}"
    
    def get_assigned_tenant(self):
        """Get the currently assigned tenant for this unit"""
        from tenants.models import Tenant
        return self.tenants.first()
    
    def get_tenant_display_name(self):
        """Get full name of assigned tenant"""
        tenant = self.get_assigned_tenant()
        if tenant:
            return f"{tenant.first_name} {tenant.last_name}"
        return None
    
    def is_occupied(self):
        """Check if unit is occupied based on assigned tenant"""
        return self.get_assigned_tenant() is not None