"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from .views import DoctorListCreateView,DoctorViewSet
from doctor_finder import views
from rest_framework.routers import DefaultRouter 
from .views import get_weather,get_coordinates

router = DefaultRouter()
router.register(r'doctor_finder', DoctorViewSet)


urlpatterns = [
     path('doctors/', DoctorListCreateView.as_view(), name='doctor-list-create'),
     path('otp/request/', views.request_otp, name='request_otp'),
     path('otp/verify/', views.verify_otp, name='verify_otp'),
     path('', include(router.urls)),
     path('weather/', get_weather, name='get_weather'),
     path('coordinates/', get_coordinates, name='get_coordinates'),
     path('repos/', views.list_repos),
     path('create-repo/', views.create_repo),
     path('', views.home, name='home'),
     path('country/', views.home, name='country'),
     path('register/', views.register, name='register'),
     path('registration/', views.register, name='register'),
     path('verify/', views.verify_otp, name='verify_otp'),
]


