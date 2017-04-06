from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from photoserver import views

urlpatterns = [
    url(r'^album/$', views.create_album),
    url(r'^photo/$', views.create_photo),
    url(r'^video/$', views.create_video),
    url(r'^photo/([^/]+/[^/]+)$', views.update_delete_photo),
    url(r'^video/([^/]+/[^/]+)$', views.update_delete_video),
    url(r'^album/([^/]+)/$', views.view_album),
    url(r'^album/([^/]+)/videos/$', views.view_videos),
    url(r'^album/([^/]+)/download/$', views.download_as_zip),
    url(r'^admin/', include(admin.site.urls)),
]

# For local testing purposes:
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
