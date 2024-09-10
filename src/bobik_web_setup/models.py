from django.db import models


# Create your models here.
class BobikSiteSetup(models.Model):
    site = models.OneToOneField("sites.Site", on_delete=models.CASCADE)

    ai_model = models.CharField(max_length=30, default="claude-3-5-sonnet-20240620")
    ai_api_key = models.CharField(max_length=255)

    admin_email = models.EmailField(
        max_length=255,
        help_text="E-mail na który będą wysyłane ankiety preanestetyczne",
    )
    admin_password = models.CharField(
        max_length=50, help_text="Poczatkowe hasło administratora"
    )
