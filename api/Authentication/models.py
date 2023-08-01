from django.db import models
from django.contrib.auth.models import User #AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db.models.signals import post_save, pre_save
from .services import unique_otp_generator
from Student_Register.models import Student_Register
from django.dispatch import receiver

class VoterOTP(models.Model):
    voter = models.OneToOneField(Student_Register, related_name="voter_otp", blank=False, null=False, on_delete=models.CASCADE)
    otp = models.CharField(max_length=10, unique=True)
    used = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Voter: {self.voter.voter_id} - OTP: {self.otp}'

# @receiver(post_save, sender=Student_Register)
# def pre_save_create_OTP(sender, instance, *args, **kwargs):
#     # print(instance.phone)
#     if instance.phone:
#         voter, created = VoterOTP.objects.get_or_create(voter=instance)
#         if not voter.otp:
#             voter.otp = unique_otp_generator(voter)
#             voter.save()
#         print(voter)
# # pre_save.connect(pre_save_create_OTP,sender=VoterOTP)	











# class UserAccountManager(BaseUserManager):
#     def create_user(self, email, name, password=None):
#         if not email:
#             raise ValueError('Users must have an email address')

#         email = self.normalize_email(email)
#         user = self.model(email=email, name=name)

#         user.set_password(password)
#         user.save()

#         return user

#     def create_superuser(self, name, email, password=None, **extra_fields):
#         user = self.create_user(name, email, password=password, **extra_fields)
#         user.is_active = True
#         user.is_staff = True
#         user.is_admin = True
#         user.save(using=self._db)
#         return user

# class UserAccount(AbstractBaseUser, PermissionsMixin):
#     email = models.EmailField(max_length=255, unique=True)
#     name = models.CharField(max_length=255)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False) 
#     is_admin = models.BooleanField(default=False)

#     objects = UserAccountManager()
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['name']

#     def get_full_name(self):
#         return self.name

#     def __str__(self):
#         return self.email