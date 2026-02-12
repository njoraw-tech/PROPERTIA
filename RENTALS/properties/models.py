from django.db import models

# Create your models here.
class Property(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    county = models.CharField(max_length=100)
    total_units = models.IntegerField(default=0)
    description = models.CharField(max_length=255)
    property_image = models.ImageField(upload_to='property_images/', blank=True, null=True)


    def __str__(self):
        return self.name