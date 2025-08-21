from django.apps import AppConfig


class DoctorFinderConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'doctor_finder'

#13) Write a Django project that uses token-based authentication for users and restricts access to certain API endpoints.
class DoctorsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'doctor_finder'

    def ready(self):
        import doctor_finder.signals
