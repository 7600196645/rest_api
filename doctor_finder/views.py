from django.shortcuts import render,redirect
from .serializers import DoctorSerializer
from rest_framework import generics,viewsets
from .models import Doctor,OTP
import random
from django.conf import settings
from twilio.rest import Client
from django.contrib.auth.decorators import login_required
import requests
from django.http import JsonResponse
import tweepy
from .forms import CountryForm,RegisterForm
from .email_utils import send_confirmation_email
from .forms import RegistrationForm, OTPForm
from .utils import send_otp
import random

# Create your views here.
#9) Write a Django project to set up a new app called doctor_finder and create models, serializers, and views.
class DoctorListCreateView(generics.ListCreateAPIView):
    queryset = Doctor.objects.all().order_by('id')
    serializer_class = DoctorSerializer

#10)Write a Django project that integrates Google login and sends OTPs to users using Twilio.
def send_otp(phone, otp):
    client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
    message = client.messages.create(
        body=f'Your OTP is {otp}',
        from_=settings.TWILIO_PHONE_NUMBER,
        to=phone
    )
    return message.sid

@login_required
def request_otp(request):
    if request.method == "POST":
        phone = request.POST.get("phone")
        otp_code = str(random.randint(100000, 999999))
        OTP.objects.update_or_create(user=request.user, defaults={
            'phone_number': phone,
            'otp_code': otp_code
        })
        send_otp(phone, otp_code)
        return redirect('verify_otp')
    return render(request, 'request_otp.html')

@login_required
def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get("otp")
        user_otp = OTP.objects.filter(user=request.user).first()
        if user_otp and user_otp.otp_code == entered_otp:
            return render(request, "otp_success.html")
        else:
            return render(request, "verify_otp.html", {"error": "Invalid OTP"})
    return render(request, 'verify_otp.html')

#11)Write a Django REST API with endpoints for creating, reading, updating, and deleting doctors.
#12)Write a Django project that allows users to create, read, update, and delete doctor profiles using API endpoints
class DoctorViewSet(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer


#14)Write a Django project to fetch current weather data for a location using the OpenWeatherMap API.
API_KEY = 'bc82d61215fc520532a718f008c460ef'  # Replace with your actual key

def get_weather(request):
    city = request.GET.get('city')
    if not city:
        return JsonResponse({'error': 'City not provided'}, status=400)

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    response = requests.get(url)
    data = response.json()

    if response.status_code != 200 or data.get("cod") != 200:
        return JsonResponse({'error': 'City not found'}, status=404)

    weather_data = {
        'city': city,
        'temperature': data['main']['temp'],
        'description': data['weather'][0]['description'],
        'humidity': data['main']['humidity'],
        'wind_speed': data['wind']['speed'],
    }

    return JsonResponse(weather_data)


#15)Write a Django project that uses Google Maps API to find the coordinates of a given address.
GOOGLE_MAPS_API_KEY = 'AIzaSyBaZmJEFBCxHQP2a3MqhFCCcpWOpZGxfWQ'  

def get_coordinates(request):
    address = request.GET.get('address')
    if not address:
        return JsonResponse({'error': 'Address parameter is required'}, status=400)

    url = f'https://maps.googleapis.com/maps/api/geocode/json'
    params = {
        'address': address,
        'key': GOOGLE_MAPS_API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    if data['status'] != 'OK':
        return JsonResponse({'error': 'Invalid address or API error'}, status=400)

    location = data['results'][0]['geometry']['location']
    return JsonResponse({
        'address': address,
        'latitude': location['lat'],
        'longitude': location['lng']
    })


import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

#16)Write a Django project that interacts with the GitHub API to create a new repository and list all repositories for a given user.
GITHUB_TOKEN = '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'

def list_repos(request):
    username = request.GET.get('username')
    if not username:
        return JsonResponse({'error': 'GitHub username is required'}, status=400)

    url = f'https://api.github.com/users/{username}/repos'
    response = requests.get(url)

    if response.status_code != 200:
        return JsonResponse({'error': 'Could not fetch repositories'}, status=500)

    repo_data = [{'name': repo['name'], 'url': repo['html_url']} for repo in response.json()]
    return JsonResponse({'repositories': repo_data})


@csrf_exempt
def create_repo(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'POST request required'}, status=405)

    data = json.loads(request.body)
    repo_name = data.get('name')
    private = data.get('private', False)

    if not repo_name:
        return JsonResponse({'error': 'Repository name is required'}, status=400)

    url = 'https://api.github.com/user/repos'
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github+json'
    }

    payload = {
        'name': repo_name,
        'private': private
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 201:
        return JsonResponse({'message': 'Repository created successfully', 'url': response.json()['html_url']})
    else:
        return JsonResponse({'error': 'Failed to create repository', 'details': response.json()}, status=400)



#17)Write a Django project to fetch and display the latest 5 tweets from a Twitter user using the Twitter API.
def get_latest_tweets(username):
    client = tweepy.Client(bearer_token=settings.TWITTER_BEARER_TOKEN)
    user = client.get_user(username=username)
    tweets = client.get_users_tweets(id=user.data.id, max_results=5, tweet_fields=["created_at"])

    return tweets.data if tweets.data else []

def home(request):
    username = 'twitterdev'  # Example Twitter handle
    tweets = get_latest_tweets(username)
    return render(request, 'home.html', {'tweets': tweets, 'username': username})



#18)Write a Django project that displays details (population, language, currency) of a country entered by the user using the REST Countries API.
def get_country_info(country_name):
    url = f"https://restcountries.com/v3.1/name/{country_name}"
    response = requests.get(url)
    if response.status_code != 200:
        return None
    data = response.json()[0]
    return {
        'name': data.get('name', {}).get('common'),
        'population': data.get('population'),
        'languages': ', '.join(data.get('languages', {}).values()),
        'currency': ', '.join([v.get('name') for v in data.get('currencies', {}).values()])
    }

def home(request):
    country_info = None
    error = None
    if request.method == 'POST':
        form = CountryForm(request.POST)
        if form.is_valid():
            country_info = get_country_info(form.cleaned_data['name'])
            if not country_info:
                error = "Country not found."
    else:
        form = CountryForm()
    return render(request, 'country.html', {'form': form, 'country_info': country_info, 'error': error})



#19)Write a Django project to send a confirmation email to a user using the SendGrid API after successful registration.
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            # Here you would save user to DB (omitted for brevity)
            send_confirmation_email(email)
            return render(request, 'success.html', {'email': email})
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})


#20)20) Write a Django project that sends an OTP to the user's mobile number during registration using Twilio API.
# Temporary storage (for demo only; use session or DB in production)
user_data = {}

def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            phone = form.cleaned_data['phone']
            name = form.cleaned_data['name']
            otp = str(random.randint(100000, 999999))
            user_data['otp'] = otp
            user_data['name'] = name
            user_data['phone'] = phone
            send_otp(phone, otp)
            return redirect('verify_otp')
    else:
        form = RegistrationForm()
    return render(request, 'registration.html', {'form': form})

def verify_otp(request):
    if request.method == 'POST':
        form = OTPForm(request.POST)
        if form.is_valid() and form.cleaned_data['otp'] == user_data.get('otp'):
            return render(request, 'reg_success.html', {'name': user_data.get('name')})
        else:
            form.add_error('otp', 'Invalid OTP')
    else:
        form = OTPForm()
    return render(request, 'verify_otp1.html', {'form': form})
