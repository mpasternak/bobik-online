from bobik.bobik import Bobik
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import UpdateView

from bobik_web_setup.models import BobikSiteSetup


# Create your views here.
class BobikWebSetupView(UpdateView):
    model = BobikSiteSetup

    fields = ["ai_model", "ai_api_key", "admin_email", "admin_password"]

    def get_object(self, queryset=None):
        try:
            return BobikSiteSetup.objects.get(site=self.request.site)
        except BobikSiteSetup.DoesNotExist:
            return BobikSiteSetup(site=self.request.site)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.pk:  # zapisany
            return HttpResponseRedirect(reverse("generate_patient_url"))
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):

        # Sprawdź, czy inicjalizacja modelu AI powiedzie się z takimi ustawieniami

        api_key = form.cleaned_data.get("ai_api_key")
        model = form.cleaned_data.get("ai_model")
        bobik = Bobik(
            system_prompt="Testuję połączenie", model=model, model_api_key=api_key
        )

        try:
            list(bobik.send_message("Witaj!"))
            self.object = form.save()
        except Exception as e:
            form.errors["ai_model"] = (
                "Problem z zapisaniem konfiguracji. Przy testach modelu wystąpił błąd: "
                + str(e)
                + ". Może to świadczyć o nieprawidłowych parametrach (nazwa modelu, "
                "klucz API), problemach z siecią lub innych problemach. "
            )
            return super().form_invalid(form)

        return HttpResponseRedirect("/")
