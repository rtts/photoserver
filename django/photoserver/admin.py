from django.contrib import admin
from .models import Album, Photo

class PhotoAdmin(admin.TabularInline):
    model = Photo
    extra = 0

@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    actions = None
    list_display = ('album_id', 'game_name', 'nr_of_photos')
    fields = ('game_name', 'partner_name', 'game_id')
    inlines = [PhotoAdmin]
