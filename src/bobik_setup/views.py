import uuid

from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import UpdateView

from bobik_setup.models import BobikSite


# Create your views here.
class BobikWebSetupView(UpdateView):
    model = BobikSite

    fields = ["ai_model", "ai_api_key", "admin_email", "admin_password"]

    def get_object(self, queryset=None):
        try:
            return BobikSite.objects.get(site=self.request.site)
        except BobikSite.DoesNotExist:
            return BobikSite(site=self.request.site)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.pk:  # zapisany
            return HttpResponseRedirect(reverse("generate_patient_url"))
        return super().get(request, *args, **kwargs)

    @transaction.atomic
    def form_valid(self, form):

        # Sprawdź, czy inicjalizacja modelu AI powiedzie się z takimi ustawieniami

        model = form.cleaned_data.get("ai_model")

        self.object = form.save(commit=False)

        try:
            self.object.send_user_message(
                msg="test", config={"configurable": {"thread_id": str(uuid.uuid4())}}
            )
            self.object = form.save(commit=True)
        except Exception as e:
            form.errors["ai_model"] = (
                "Problem z zapisaniem konfiguracji. Przy testach podłączenia do LLM "
                + model
                + "  wystąpił błąd: "
                + str(e)
                + ". Może to świadczyć o nieprawidłowych parametrach (nazwa modelu, "
                "klucz API), problemach z siecią lub innych problemach. "
            )
            return super().form_invalid(form)

        try:
            User.objects.create_superuser(
                "admin",
                email=form.cleaned_data["admin_email"],
                password=form.cleaned_data["admin_password"],
            )
        except IntegrityError as e:
            form.errors["admin_email"] = (
                f"Problem z utworzeniem konta admina ({e}; prawdopodobnei konto admin "
                "już istnieje. W tej sytuacji ten formularz w ogóle nie powinien się "
                "pojawiać... skontaktuj się z administratorem?"
            )
            return super().form_invalid(form)

        return HttpResponseRedirect("/")
