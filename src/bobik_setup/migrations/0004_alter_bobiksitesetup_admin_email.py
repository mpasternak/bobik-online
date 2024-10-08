# Generated by Django 5.1.1 on 2024-09-10 14:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bobik_setup", "0003_bobiksitesetup_admin_password"),
    ]

    operations = [
        migrations.AlterField(
            model_name="bobiksitesetup",
            name="admin_email",
            field=models.EmailField(
                help_text="E-mail na który będą wysyłane ankiety preanestetyczne",
                max_length=255,
            ),
        ),
    ]
