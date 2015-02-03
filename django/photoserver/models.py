import random
import string
from django.db import models

ALBUM_URL_LENGTH = 32
PHOTO_FILENAME_LENGTH = 32

def random_string(length):
    """Returns a random alphanumeric string"""
    return ''.join(random.choice(string.ascii_letters + string.digits) for x in range(length))

def photo_location(obj, filename):
    """Returns a photo's upload location"""
    return '/'.join([obj.album.album_id(), random_string(PHOTO_FILENAME_LENGTH) + '.jpg'])

class Album(models.Model):
    """A photo album"""
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    game_name = models.CharField(max_length=255)
    partner_name = models.SlugField()
    game_id = models.IntegerField()
    album_url = models.CharField(max_length=ALBUM_URL_LENGTH, blank=True)

    def album_id(self):
        """Returns the album id"""
        return self.partner_name + str(self.game_id)

    def nr_of_photos(self):
        """Returns the number of photos"""
        return self.photos.count()

    def save(self, *args, **kwargs):
        """Overrides the save method to generate a random album URL'"""
        if self.pk is None:
            self.album_url = random_string(ALBUM_URL_LENGTH)
        super(Album, self).save(*args, **kwargs)

    def __str__(self):
        return self.album_id()

    class Meta:
        unique_together = ('partner_name', 'game_id')

class Photo(models.Model):
    """A photo"""
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    source = models.ImageField(upload_to=photo_location)
    comment = models.CharField(max_length=255, blank=True)
    album = models.ForeignKey(Album, related_name='photos')

    def __str__(self):
        return self.source.url
