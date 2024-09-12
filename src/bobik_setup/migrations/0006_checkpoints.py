# Generated by Django 5.1.1 on 2024-09-12 20:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("bobik_setup", "0005_rename_bobiksitesetup_bobiksite"),
    ]

    operations = [
        migrations.CreateModel(
            name="Checkpoints",
            fields=[
                ("thread_id", models.TextField()),
                ("checkpoint_ns", models.TextField()),
                ("checkpoint_id", models.TextField(primary_key=True, serialize=False)),
                ("parent_checkpoint_id", models.TextField()),
                ("type", models.TextField()),
                ("checkpoint", models.JSONField()),
                ("metadata", models.JSONField()),
            ],
            options={
                "db_table": "checkpoints",
                "managed": False,
            },
        ),
    ]
