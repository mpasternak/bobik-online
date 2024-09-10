import uuid

from bobik.bobik import Bobik
from bobik.prompt import get_prompt
from bobik_web_setup.models import BobikSiteSetup
from django.db import models


class BobikChatParameters(models.Model):
    thread_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    imie_pacjenta = models.CharField(max_length=100)
    jezyk_pacjenta = models.CharField(max_length=30, default="polski")

    plec_pacjenta = models.CharField(max_length=50, default="mężczyzna")
    wiek_pacjenta = models.PositiveSmallIntegerField(default=45)
    tryb_zabiegu = models.CharField(max_length=50, default="planowy")
    rodzaj_zabiegu = models.CharField(max_length=150, default="cholecystektomia")

    prompt_sent = models.BooleanField(default=False)

    def get_bobik_chat(self):
        site_setup = BobikSiteSetup.objects.get(site_id=1)

        ret = Bobik(
            get_prompt(
                imie_pacjenta=self.imie_pacjenta,
                jezyk_pacjenta=self.jezyk_pacjenta,
                plec_pacjenta=self.plec_pacjenta,
                wiek_pacjenta=self.wiek_pacjenta,
                tryb_zabiegu=self.tryb_zabiegu,
                rodzaj_zabiegu=self.rodzaj_zabiegu,
                email_to=site_setup.admin_email,
            )
            + " Zawsze odpowiadaj tekstem w formacie RST. ",
            thread_id=str(self.thread_id),
            db_url="postgres://localhost/",
            model=site_setup.ai_model,
            model_api_key=site_setup.ai_api_key,
        )

        if not self.prompt_sent:
            list(ret.say_hello())
            self.prompt_sent = True
            self.save(update_fields=["prompt_sent"])

        return ret
