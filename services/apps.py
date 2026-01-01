from django.apps import AppConfig
from django.db.models.signals import post_migrate


def create_default_genders(sender, **kwargs):
    from .models import Gender
    defaults = ["male", "female"]
    for g in defaults:
        Gender.objects.get_or_create(name=g)


class ServicesConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "services"

    def ready(self):
        post_migrate.connect(create_default_genders, sender=self)


