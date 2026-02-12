from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    # Role Choices
    ADMIN = 'admin'
    LANDLORD = 'landlord'
    CARETAKER = 'caretaker'
    BOOKKEEPER = 'bookkeeper'
    
    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (LANDLORD, 'Landlord'),
        (CARETAKER, 'Caretaker'),
        (BOOKKEEPER, 'Bookkeeper'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=LANDLORD) # New Field
    phone_number = models.CharField(max_length=15, blank=True)
    avatar = models.ImageField(upload_to='avatars/', default='default_avatar.png')
    notification_enabled = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username}'s Profile ({self.get_role_display()})"

# Signals to handle profile creation/saving
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


