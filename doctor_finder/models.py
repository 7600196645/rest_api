from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Doctor(models.Model):
    name=models.CharField(max_length=100)
    specialization = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    location = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.specialization}"
    

class OTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
