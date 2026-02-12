from django.db import models

# Create your models here.
import uuid
from units.models import Unit
from tenants.models import Tenant

class Invoice(models.Model):
    STATUS_CHOICES = [('Paid', 'Paid'), ('Unpaid', 'Unpaid')]
    TYPE_CHOICES = [('Rent', 'Rent'), ('Water', 'Water'), ('Service', 'Service')]

    invoice_number = models.CharField(max_length=50, unique=True, editable=False)
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE)
    tenant = models.ForeignKey(Tenant, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='Rent')
    due_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Unpaid')

    def save(self, *args, **kwargs):
        if not self.invoice_number:
            # Matches your screenshot format: INV-YearMonth-ShortUUID
            self.invoice_number = f"INV-{self.due_date.strftime('%Y%m')}-{uuid.uuid4().hex[:8]}"
        super().save(*args, **kwargs)