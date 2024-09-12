from django.contrib import admin

from bobik_prompts.models import BobikPrompt


@admin.register(BobikPrompt)
class BobikPromptAdmin(admin.ModelAdmin):
    list_display = ("rodzaj", "tresc")
    search_fields = ["tresc"]
