from anthropic import APIConnectionError
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView
from docutils.core import publish_parts
from docutils.utils import Reporter
from openai import APIConnectionError as OpenAIAPIConnectionError

from bobik_web_chat.models import BobikChat


def rst_to_html(rst_string):
    return (
        publish_parts(
            rst_string,
            writer_name="html",
            settings_overrides={"report_level": Reporter.SEVERE_LEVEL + 1},
        )
        .get("body", "")
        .strip()
    )


class UtworzLinkDlaPacjenta(CreateView):
    model = BobikChat
    fields = [
        "imie_pacjenta",
        "wiek_pacjenta",
        "plec_pacjenta",
        "tryb_zabiegu",
        "rodzaj_zabiegu",
        "jezyk_pacjenta",
    ]

    def get_success_url(self):
        return reverse("show_patient_url", kwargs={"pk": str(self.object.thread_id)})


class PokazLinkDlaPacjenta(DetailView):
    model = BobikChat

    def get_context_data(self, **kwargs):
        kwargs["full_site"] = self.request.META.get("HTTP_HOST")
        return kwargs


class BobikChatView(DetailView):
    model = BobikChat
    template_name = "bobik_web_chat/bobikchat_chat.html"

    def get_chat(self):
        self.object: BobikChat = self.get_object()
        self.object.start_bobik_chat()
        return self.object

    def post(self, request, *args, **kwargs):
        if request.POST.get("msg"):
            try:
                list(self.get_chat().send_message(request.POST.get("msg")))
            except (OpenAIAPIConnectionError, APIConnectionError) as e:
                messages.add_message(
                    request,
                    messages.INFO,
                    "Wystąpił błąd połączenia z API AI - " + str(e) + ". "
                    "Spróbuj później. Twój komunikat prawdopodobnie nie został wysłany. "
                )

        return HttpResponseRedirect(".")

    def get_context_data(self, **kwargs):
        chat = self.get_chat()

        for elem in chat.get_messages():
            # Przeskocz 2 komunikaty z listy. Pierwszy to prompt systemowy,
            # drugi to komunikat "Przywitaj się", bo bez tego AI będzie milczeć.
            messages = list(list(elem.checkpoint["channel_values"]["messages"][2:]))
            kwargs["bobik_messages"] = messages
            for message in kwargs["bobik_messages"]:
                if message.type == "human":
                    continue

                if type(message.content) == list:
                    message.content = rst_to_html(message.content[0].get("text"))
                else:
                    message.content = rst_to_html(message.content)

            break

        return kwargs
