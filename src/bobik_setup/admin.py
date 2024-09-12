from django.contrib import admin

from bobik_setup.models import BobikSite, Checkpoints


# Register your models here.
@admin.register(BobikSite)
class BobikSiteAdmin(admin.ModelAdmin):
    pass

@admin.register(Checkpoints)
class CheckpointsAdmin(admin.ModelAdmin):
    search_fields = ['thread_id']
    list_display = ['thread_id', 'metadata']
    pass