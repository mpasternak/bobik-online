# Generated by Django 5.1.1 on 2024-09-11 17:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("bobik_setup", "0004_alter_bobiksitesetup_admin_email"),
        ("sites", "0002_alter_domain_unique"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="BobikSiteSetup",
            new_name="BobikSite",
        ),
    ]
