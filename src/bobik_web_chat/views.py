from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView, DetailView
from docutils.core import publish_parts
from docutils.utils import Reporter

from bobik_web_chat.models import BobikChatParameters


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
    model = BobikChatParameters
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
    model = BobikChatParameters

    def get_context_data(self, **kwargs):
        kwargs["full_site"] = self.request.META.get("HTTP_HOST")
        return kwargs


class BobikChat(DetailView):
    model = BobikChatParameters
    template_name = "bobik_web_chat/bobikchatparameters_chat.html"

    def get_chat(self):
        self.object = self.get_object()
        self.chat = self.object.get_bobik_chat()
        return self.chat

    def post(self, request, *args, **kwargs):
        chat = self.get_chat()
        if request.POST.get("msg"):
            list(self.chat.send_message(request.POST.get("msg")))
        return HttpResponseRedirect(".")

    def get_context_data(self, **kwargs):
        chat = self.get_chat()

        for elem in chat.get_messages():
            messages = list(list(elem.checkpoint["channel_values"]["messages"][1:]))
            kwargs["messages"] = messages
            for message in kwargs["messages"]:
                if message.type == "human":
                    continue

                if type(message.content) == list:
                    message.content = rst_to_html(message.content[0].get("text"))
                else:
                    message.content = rst_to_html(message.content)

            break

        return kwargs
