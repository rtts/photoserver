from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from photoserver import views

urlpatterns = [
    url(r'^album/$', views.create_album),
    url(r'^photo/$', views.create_photo),
    url(r'^album/([^/]+)/photo/([^/]+)/$', views.update_delete_photo),
    url(r'^album/([^/]+)/$', views.view_album),
    url(r'^admin/', include(admin.site.urls)),
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]
