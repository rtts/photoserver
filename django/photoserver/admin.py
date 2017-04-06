from django.contrib import admin
from .models import Album, Photo, Video

class PhotoAdmin(admin.TabularInline):
    model = Photo
    extra = 0

class VideoAdmin(admin.TabularInline):
    model = Video
    extra = 0

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    actions = None
    list_display = ('album_id', 'album_url', 'game_name', 'nr_of_photos', 'nr_of_videos')
    list_filter = ('partner_name', )
    fields = ('game_name', 'partner_name', 'game_id', )
    inlines = [PhotoAdmin, VideoAdmin]
