# Generated by Django 2.0.8 on 2018-09-22 02:08

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('concordia', '0021_auto_20180922_0202'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('importer', '0010_auto_20180920_2013'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImportItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('last_started', models.DateTimeField(blank=True, null=True, verbose_name='Last time when a worker started processing this job')),
                ('completed', models.DateTimeField(blank=True, null=True, verbose_name='Time when the job completed processing')),
                ('failed', models.DateTimeField(blank=True, null=True, verbose_name='Time when the job failed and will not be restarted')),
                ('status', models.TextField(blank=True, null=True, verbose_name='Status message, if any, from the last worker')),
                ('task_id', models.UUIDField(blank=True, null=True, verbose_name='UUID of the last Celery task to process this record')),
                ('url', models.URLField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='concordia.Item')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ImportItemAsset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('last_started', models.DateTimeField(blank=True, null=True, verbose_name='Last time when a worker started processing this job')),
                ('completed', models.DateTimeField(blank=True, null=True, verbose_name='Time when the job completed processing')),
                ('failed', models.DateTimeField(blank=True, null=True, verbose_name='Time when the job failed and will not be restarted')),
                ('status', models.TextField(blank=True, null=True, verbose_name='Status message, if any, from the last worker')),
                ('task_id', models.UUIDField(blank=True, null=True, verbose_name='UUID of the last Celery task to process this record')),
                ('url', models.URLField()),
                ('sequence_number', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('asset', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='concordia.Asset')),
                ('import_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assets', to='importer.ImportItem')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ImportJob',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('last_started', models.DateTimeField(blank=True, null=True, verbose_name='Last time when a worker started processing this job')),
                ('completed', models.DateTimeField(blank=True, null=True, verbose_name='Time when the job completed processing')),
                ('failed', models.DateTimeField(blank=True, null=True, verbose_name='Time when the job failed and will not be restarted')),
                ('status', models.TextField(blank=True, null=True, verbose_name='Status message, if any, from the last worker')),
                ('task_id', models.UUIDField(blank=True, null=True, verbose_name='UUID of the last Celery task to process this record')),
                ('source_url', models.URLField(verbose_name='Source URL for the entire job')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='concordia.Project')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.RemoveField(
            model_name='campaignitemassetcount',
            name='campaign_task',
        ),
        migrations.RemoveField(
            model_name='campaigntaskdetails',
            name='project',
        ),
        migrations.DeleteModel(
            name='CampaignItemAssetCount',
        ),
        migrations.DeleteModel(
            name='CampaignTaskDetails',
        ),
        migrations.AddField(
            model_name='importitem',
            name='job',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='importer.ImportJob'),
        ),
    ]
