from django.db import models
from Profiles.models import Profile
from django.db.utils import IntegrityError

# Create your models here.
class Student_Register(models.Model):
    student_id=models.CharField(max_length=15, unique=True, blank=False, null=False)
    phone = models.CharField(max_length=20, blank=True, unique=True)
    first_name = models.CharField(max_length=15, blank=True, null=True)
    last_name = models.CharField(max_length=15, blank=True, null=True)
    other_name = models.CharField(max_length=50, blank=True)
    photo = models.ImageField(upload_to="students",blank=True)
    is_verified = models.BooleanField(default=False)
    # has_voted = models.BooleanField(default=False)
    verified_by = models.ForeignKey(Profile, related_name="student_verified", on_delete=models.CASCADE,blank=True, null=True)
    
    def __str__(self) -> str:
        return str(self.student_id)

    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
        except IntegrityError:
            # Handle the unique constraint violation
            # You can choose to raise a validation error, log the error, or take any other necessary action
            # Here's an example of raising a validation error
            # raise ValueError('The value for unique_field must be unique.')
            pass


