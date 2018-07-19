# Generated by Django 2.0.7 on 2018-07-12 18:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("concordia", "0003_collection_is_active")]

    operations = [
        migrations.AlterField(
            model_name="asset",
            name="status",
            field=models.CharField(
                choices=[
                    ("Edit", "Open for Edit"),
                    ("Submitted", "Submitted for Review"),
                    ("Completed", "Transcription Completed"),
                ],
                default="Edit",
                max_length=4,
            ),
        ),
        migrations.AlterField(
            model_name="collection",
            name="status",
            field=models.CharField(
                choices=[
                    ("Edit", "Open for Edit"),
                    ("Submitted", "Submitted for Review"),
                    ("Completed", "Transcription Completed"),
                ],
                default="Edit",
                max_length=4,
            ),
        ),
        migrations.AlterField(
            model_name="subcollection",
            name="status",
            field=models.CharField(
                choices=[
                    ("Edit", "Open for Edit"),
                    ("Submitted", "Submitted for Review"),
                    ("Completed", "Transcription Completed"),
                ],
                default="Edit",
                max_length=4,
            ),
        ),
        migrations.AlterField(
            model_name="transcription",
            name="status",
            field=models.CharField(
                choices=[
                    ("Edit", "Open for Edit"),
                    ("Submitted", "Submitted for Review"),
                    ("Completed", "Transcription Completed"),
                ],
                default="Edit",
                max_length=4,
            ),
        ),
    ]