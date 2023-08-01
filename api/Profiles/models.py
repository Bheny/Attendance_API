from django.db import models
from django.contrib.auth.models import User 
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver 

class Account(models.Model):
    title=models.CharField(max_length=255) 
    description=models.TextField(blank=True)
    is_active=models.BooleanField(default=True)
    created_on=models.DateField(auto_now_add=True)
    upadated_on=models.DateField(auto_now=True)

    def __str__(self):
        return self.title

class Profile(models.Model):
    user = models.ForeignKey(User,related_name="Profile", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/profile/', blank=True)
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female')])
    date_of_birth = models.DateField(auto_now=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    short_bio = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True) 
    address = models.TextField(blank=True, null=True)
    employee_id = models.CharField(max_length=20)

    def __str__(self):
        return self.user

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    # on create of user account, check if there is an existing profile.
    if created:
        profile = Profile.objects.create(user=instance)
        
 
