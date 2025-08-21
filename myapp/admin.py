from django.contrib import admin
from .models import Doctor

# Register your models here.
#8) Write a Django project that connects to an SQLite database and stores doctor profiles.
admin.site.register(Doctor)