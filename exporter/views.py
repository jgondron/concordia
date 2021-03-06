import csv
import os
import shutil

import bagit
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from concordia.models import Asset, Campaign, Transcription, UserAssetTagCollection
from concordia.storage import ASSET_STORAGE


class ExportCampaignToCSV(TemplateView):
    """
    Exports the transcription and tags to csv file

    """

    template_name = "transcriptions/campaign.html"

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        campaign = Campaign.objects.get(slug=self.kwargs["campaign_slug"])
        asset_list = Asset.objects.filter(item__project__campaign=campaign).order_by(
            "title", "sequence"
        )
        # Create the HttpResponse object with the appropriate CSV header.
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="{0}.csv"'.format(
            campaign.slug
        )
        field_names = ["title", "description", "media_url"]
        writer = csv.writer(response)
        writer.writerow(
            ["Campaign", "Title", "Description", "MediaUrl", "Transcription", "Tags"]
        )
        for asset in asset_list:
            transcription = Transcription.objects.filter(
                asset=asset, user=self.request.user
            )
            if transcription:
                transcription = transcription[0].text
            else:
                transcription = ""
            tags = UserAssetTagCollection.objects.filter(
                asset=asset, user=self.request.user
            )
            if tags:
                tags = list(tags[0].tags.all().values_list("name", flat=True))
            else:
                tags = ""
            row = (
                [campaign.title]
                + [getattr(asset, i) for i in field_names]
                + [transcription, tags]
            )
            writer.writerow(row)
        return response


class ExportCampaignToBagit(TemplateView):
    """
    Creates temp directory structure for source data.  Copies source image
    file from S3 or local storage into temp directory, builds export.csv
    with meta, transcription, and tag data.  Executes bagit.py to turn temp
    directory into bagit strucutre.  Builds and exports bagit structure as
    zip.  Removes all temporary directories and files.

    """

    include_images = True
    template_name = "transcriptions/campaign.html"

    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        campaign = Campaign.objects.get(slug=self.kwargs["campaign_slug"])
        asset_list = Asset.objects.filter(item__project__campaign=campaign).order_by(
            "title", "sequence"
        )

        # FIXME: this code should be working in a separate path than the media root!
        # FIXME: we should be able to export at the project and item level, too
        export_base_dir = os.path.join(settings.MEDIA_ROOT, "exporter", campaign.slug)

        for asset in asset_list:
            src = os.path.join(
                settings.MEDIA_ROOT,
                asset.item.project.campaign.slug,
                asset.item.project.slug,
                asset.item.item_id,
                asset.slug,
                asset.media_url,
            )
            dest_folder = os.path.join(
                export_base_dir, asset.item.project.slug, asset.item.item_id, asset.slug
            )
            os.makedirs(dest_folder, exist_ok=True)
            dest = os.path.join(dest_folder, asset.media_url)

            if self.include_images:
                with open(dest, mode="wb") as dest_file:
                    with ASSET_STORAGE.open(src, mode="rb") as src_file:
                        for chunk in src_file.chunks(1048576):
                            dest_file.write(chunk)

            # Get transcription data
            # FIXME: if we're not including all transcriptions, we should pick the completed or latest versions!

            try:
                transcription = Transcription.objects.get(
                    asset=asset, user=self.request.user
                ).text
            except Transcription.DoesNotExist:
                transcription = ""

            # Build transcription output text file
            tran_output_path = os.path.join(
                dest_folder, "%s.txt" % os.path.basename(asset.media_url)
            )
            with open(tran_output_path, "w") as f:
                f.write(transcription)

        # Turn Structure into bagit format
        bagit.make_bag(export_base_dir, {"Contact-Name": request.user.username})

        # Build .zip file of bagit formatted Campaign Folder
        archive_name = export_base_dir
        shutil.make_archive(archive_name, "zip", export_base_dir)

        # Download zip
        with open("%s.zip" % export_base_dir, "rb") as zip_file:
            response = HttpResponse(zip_file, content_type="application/zip")
        response["Content-Disposition"] = "attachment; filename=%s.zip" % campaign.slug

        # Clean up temp folders & zipfile once exported
        shutil.rmtree(export_base_dir)
        os.remove("%s.zip" % export_base_dir)

        return response
