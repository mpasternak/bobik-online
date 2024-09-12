import uuid

from bobik_prompts.models import BobikPrompt
from bobik_setup.models import BobikSite
from django.db import models


class BobikChat(models.Model):
    thread_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    imie_pacjenta = models.CharField(max_length=100)
    jezyk_pacjenta = models.CharField(max_length=30, default="polski")

    plec_pacjenta = models.CharField(max_length=50, default="mężczyzna")
    wiek_pacjenta = models.PositiveSmallIntegerField(default=45)
    tryb_zabiegu = models.CharField(max_length=50, default="planowy")
    rodzaj_zabiegu = models.CharField(max_length=150, default="cholecystektomia")

    prompt_sent = models.BooleanField(default=False)

    @property
    def config(self):
        return {"configurable": {"thread_id": str(self.thread_id)}}

    @property
    def site_setup(self):
        return BobikSite.objects.get(site_id=1)

    def start_bobik_chat(self):
        if not self.prompt_sent:
            system_prompt = BobikPrompt.objects.get(
                rodzaj=BobikPrompt.PromptType.WYWIAD_PREANESTETYCZNY
            ).format(
                imie_pacjenta=self.imie_pacjenta,
                jezyk_pacjenta=self.jezyk_pacjenta,
                plec_pacjenta=self.plec_pacjenta,
                wiek_pacjenta=self.wiek_pacjenta,
                tryb_zabiegu=self.tryb_zabiegu,
                rodzaj_zabiegu=self.rodzaj_zabiegu,
                email_to=self.site_setup.admin_email,
            )

            self.site_setup.send_system_message(self.config, system_prompt)

            self.prompt_sent = True
            self.save(update_fields=["prompt_sent"])

    def send_message(self, msg):
        return self.site_setup.send_user_message(self.config, msg)

    def get_messages(self):
        return self.site_setup.get_checkpointer().list(config=self.config)
