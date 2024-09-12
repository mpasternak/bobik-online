from django.db import models


class BobikPrompt(models.Model):
    class PromptType(models.IntegerChoices):
        WYWIAD_PREANESTETYCZNY = 1, "wywiad preanestetyczny"
        BADANIA_PRZED_OPERACJA = 2, "badania przed operacją"

    rodzaj = models.PositiveSmallIntegerField(choices=PromptType.choices, unique=True)
    tresc = models.TextField()

    def format(self, **kwargs):
        return self.tresc.format(**kwargs)
