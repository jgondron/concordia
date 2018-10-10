# Generated by Django 2.0.9 on 2018-10-10 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("concordia", "0003_auto_20181004_2103")]

    operations = [
        migrations.AddField(
            model_name="campaign",
            name="thumbnail_image",
            field=models.ImageField(
                blank=True, null=True, default="", upload_to="campaign-thumbnails"
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="project",
            name="thumbnail_image",
            field=models.ImageField(
                blank=True, null=True, default="", upload_to="project-thumbnails"
            ),
            preserve_default=False,
        ),
    ]
