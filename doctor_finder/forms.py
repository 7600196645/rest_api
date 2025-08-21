from django import forms

class CountryForm(forms.Form):
    name = forms.CharField(label='Country Name', max_length=100)

class RegisterForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)

class RegistrationForm(forms.Form):
    name = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=15)

class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6)
