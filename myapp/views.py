from django.shortcuts import render
from rest_framework import generics
from .models import Doctor
from myapp.serializers import DoctorSerializer

# Create your views here.

#3) Write a Django REST API to serialize a Doctor model with fields like name, specialty, and contact details.
#4) Write a Django project where the API accepts a POST request to add a doctor’s details to the database.
#5) Write a Django project that implements a class-based view to handle doctor profile creation, reading, updating, and deletion (CRUD operations).
#6) Write a Django project that routes URLs to the views handling doctor CRUD operations (/doctors, /doctors/<id>).
class DoctorListCreateView(generics.ListCreateAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

class DoctorRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

#7)Write a Django API that returns paginated results for a list of doctors.
class DoctorListView(generics.ListAPIView):
    queryset = Doctor.objects.all().order_by('id')
    serializer_class = DoctorSerializer