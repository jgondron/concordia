from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.http import Http404, HttpResponseForbidden
from django.urls import include, path, re_path
from django.views.defaults import page_not_found, permission_denied, server_error
from machina.app import board

from concordia.admin import admin_bulk_import_view
from exporter import views as exporter_views

from . import views, views_ws

for key, value in getattr(settings, "ADMIN_SITE", {}).items():
    setattr(admin.site, key, value)


tx_urlpatterns = (
    [
        path("", views.CampaignListView.as_view(), name="campaigns"),
        path("<slug:slug>/", views.CampaignDetailView.as_view(), name="campaign"),
        re_path(
            r"^alternateasset/$",
            views.ConcordiaAlternateAssetView.as_view(),
            name="alternate-asset",
        ),
        path(
            "exportCSV/<slug:campaign_slug>/",
            exporter_views.ExportCampaignToCSV.as_view(),
            name="export-csv",
        ),
        path(
            "exportBagIt/<slug:campaign_slug>/",
            exporter_views.ExportCampaignToBagit.as_view(),
            name="export-bagit",
        ),
        path(
            "<slug:campaign_slug>/report/",
            views.ReportCampaignView.as_view(),
            name="campaign-report",
        ),
        path(
            "<slug:campaign_slug>/<slug:project_slug>/<slug:item_id>/<slug:slug>/",
            views.ConcordiaAssetView.as_view(),
            name="asset-detail",
        ),
        path(
            "<slug:campaign_slug>/<slug:slug>/",
            views.ConcordiaProjectView.as_view(),
            name="project-detail",
        ),
        path(
            "<slug:campaign_slug>/<slug:project_slug>/<slug:item_id>/",
            views.ItemDetailView.as_view(),
            name="item-detail",
        ),
    ],
    "transcriptions",
)

urlpatterns = [
    path("", views.HomeView.as_view(), name="homepage"),
    path("healthz", views.healthz, name="health-check"),
    path("about/", views.static_page, name="about"),
    path("instructions/", views.static_page, name="instructions"),
    path("for-educators/", views.static_page, name="for-educators"),
    path("latest/", views.static_page, name="latest"),
    path("contact/", views.ContactUsView.as_view(), name="contact"),
    path("campaigns/", include(tx_urlpatterns, namespace="transcriptions")),
    path(
        "reserve-asset-for-transcription/<int:asset_pk>/",
        views.reserve_asset_transcription,
        name="reserve-asset-for-transcription",
    ),
    path(
        "assets/<int:asset_pk>/transcriptions/save/",
        views.save_transcription,
        name="save-transcription",
    ),
    path(
        "transcriptions/<int:pk>/submit/",
        views.submit_transcription,
        name="submit-transcription",
    ),
    path(
        "transcriptions/<int:pk>/review/",
        views.review_transcription,
        name="review-transcription",
    ),
    path(
        "assets/<int:asset_pk>/tags/",
        views_ws.UserAssetTagsGet().as_view(),
        name="get-tags",
    ),
    path(
        "assets/<int:asset_pk>/tags/submit/",
        views_ws.TagCreate.as_view(),
        name="submit-tags",
    ),
    re_path(
        r"^account/register/$",
        views.ConcordiaRegistrationView.as_view(),
        name="registration_register",
    ),
    re_path(
        r"^account/profile/$", views.AccountProfileView.as_view(), name="user-profile"
    ),
    url(r"^accounts/", include("django_registration.backends.activation.urls")),
    url(r"^accounts/", include("django.contrib.auth.urls")),
    # TODO: when we upgrade to Django 2.1 we can use the admin site override
    # mechanism (the old one is broken in 2.0): see https://code.djangoproject.com/ticket/27887
    path("admin/bulk-import", admin_bulk_import_view, name="admin-bulk-import"),
    path("admin/", admin.site.urls),
    # Apps
    path("forum/", include(board.urls)),
    path("captcha/", include("captcha.urls")),
    re_path(r"^password_reset/$", auth_views.password_reset, name="password_reset"),
    re_path(
        r"^password_reset/done/$",
        auth_views.password_reset_done,
        name="password_reset_done",
    ),
    re_path(
        r"^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$",
        auth_views.password_reset_confirm,
        name="password_reset_confirm",
    ),
    re_path(
        r"^reset/done/$",
        auth_views.password_reset_complete,
        name="password_reset_complete",
    ),
    # Internal support assists:
    path("maintenance-mode/", include("maintenance_mode.urls")),
    path("error/500/", server_error),
    path("error/404/", page_not_found, {"exception": Http404()}),
    path("error/403/", permission_denied, {"exception": HttpResponseForbidden()}),
    url("", include("django_prometheus_metrics.urls")),
    url(r"^robots\.txt", include("robots.urls")),
]

if settings.DEBUG:
    import debug_toolbar
    from django.conf.urls.static import static

    urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
