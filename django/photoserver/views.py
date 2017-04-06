"""
This module implements the API calls. The API documentation is available at either doc/index.rst or static/doc/html/index.html
"""

import os
import io
import json
import base64
import zipfile

from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from django.conf import settings

from .utils import http_auth_required
from .models import Album, Photo

ENCODING = "utf-8"
FALLBACKENCODING = "latin-1"
HTTP_AUTH_REALM = "Photoserver-API"
ERROR_JSON = 'You are sending invalid JSON! The exact error is: "{}"'
ERROR_KEY = 'The request doesn’t contain the required arguments. At least the following key is missing: {}'
ERROR_BASE64 = 'The Jpeg data couldn’t be decoded using base64. The exact error is: "{}"'
ERROR_JPG = 'The image you supplied is not a valid image. Is the Jpeg data corrupted?'
ERROR_409 = "The specified album already exists."

@csrf_exempt
@http_auth_required(realm=HTTP_AUTH_REALM)
@require_http_methods(['POST'])
def create_album(request):
    """Create a new photo album"""

    try:
        data = json.loads(request.body.decode(ENCODING))
    except ValueError as e:
        try:
            data = json.loads(request.body.decode(FALLBACKENCODING))
        except ValueError as e:
            return HttpResponseBadRequest(ERROR_JSON.format(e))

    try:
        try:
            album = Album.objects.get(
                partner_name = data['partnerName'],
                game_id = data['gameId'],
            )
            is_new = False
            if album.game_name != data['gameName']:
                return HttpResponse(
                    "That album exists, but the name is different than the name you sent!",
                    content_type="text/plain",
                    status=412
                )
        except Album.DoesNotExist:
            album = Album(
                game_name = data['gameName'],
                partner_name = data['partnerName'],
                game_id = data['gameId'],
            )
            album.save()
            is_new = True
    except KeyError as e:
        return HttpResponseBadRequest(ERROR_KEY.format(e))

    return JsonResponse({
        'albumId': album.album_id,
        'albumUrl': album.album_url,
        }, status=(200 if is_new else 409))

@csrf_exempt
@http_auth_required(realm=HTTP_AUTH_REALM)
@require_http_methods(['POST'])
def create_photo(request):
    """Add a new photo to an album"""

    # Cautiously extract and decode request data
    try:
        data = json.loads(request.body.decode(ENCODING))
    except ValueError as e:
        try:
            data = json.loads(request.body.decode(FALLBACKENCODING))
        except ValueError as e:
            return HttpResponseBadRequest(ERROR_JSON.format(e))
    try:
        album = get_object_or_404(Album, album_id=data['albumId'])
        encoded_jpg = data['jpgData']
    except KeyError as e:
        return HttpResponseBadRequest(ERROR_KEY.format(e))
    try:
        decoded_jpg = base64.b64decode(data['jpgData'], validate=False)
    except Exception as e:
        return HttpResponseBadRequest(ERROR_BASE64.format(e))

    # Create and validate the photo object
    photo = Photo(
        album = album,
        source = ContentFile(decoded_jpg, 'ignoredfilename.jpg'),
    )
    try:
        photo.source.width; # triggers the image validation
    except TypeError:
        return HttpResponseBadRequest(ERROR_JPG)

    # Save photo to database and return successfully
    if 'comment' in data:
        photo.comment = data['comment']
    photo.save()
    return JsonResponse({
        'photoUrl': photo.source.name,
        })

@csrf_exempt
@http_auth_required(realm=HTTP_AUTH_REALM)
@require_http_methods(['POST'])
def create_video(request):
    """Add a new video to an album"""

    # Cautiously extract and decode request data
    try:
        data = json.loads(request.body.decode(ENCODING))
    except ValueError as e:
        try:
            data = json.loads(request.body.decode(FALLBACKENCODING))
        except ValueError as e:
            return HttpResponseBadRequest(ERROR_JSON.format(e))
    try:
        album = get_object_or_404(Album, album_id=data['albumId'])
        filetype = data['filetype']
        encoded_video = data['videoData']
    except KeyError as e:
        return HttpResponseBadRequest(ERROR_KEY.format(e))
    try:
        decoded_video = base64.b64decode(data['videoData'], validate=False)
    except Exception as e:
        return HttpResponseBadRequest(ERROR_BASE64.format(e))

    # Create the video object
    video = Video(
        album = album,
        source = ContentFile(decoded_video, 'ignoredfilename.' + filetype),
    )

    # Save video to database and return successfully
    if 'title' in data:
        video.title = data['title']
    if 'comment' in data:
        video.comment = data['comment']
    video.save()
    return JsonResponse({
        'videoUrl': video.source.name,
    })

@csrf_exempt
@http_auth_required(realm=HTTP_AUTH_REALM)
@require_http_methods(['PUT', 'DELETE'])
def update_delete_photo(request, photo_url):
    if request.method == 'PUT':
        return update_photo(request, photo_url)
    elif request.method == 'DELETE':
        return delete_photo(request, photo_url)

@csrf_exempt
@http_auth_required(realm=HTTP_AUTH_REALM)
@require_http_methods(['PUT', 'DELETE'])
def update_delete_video(request, video_url):
    if request.method == 'PUT':
        return update_video(request, video_url)
    elif request.method == 'DELETE':
        return delete_video(request, video_url)

def update_photo(request, photo_url):
    """Update the comment on an existing photo"""

    try:
        data = json.loads(request.body.decode(ENCODING))
    except ValueError as e:
        try:
            data = json.loads(request.body.decode(FALLBACKENCODING))
        except ValueError as e:
            return HttpResponseBadRequest(ERROR_JSON.format(e))
    try:
        comment = data['comment']
    except KeyError as e:
        return HttpResponseBadRequest(ERROR_KEY.format(e))

    photo = get_object_or_404(Photo, source=photo_url)
    photo.comment = comment
    photo.save()

    return HttpResponse()

def update_video(request, video_url):
    """Update the title and/or comment on an existing video"""

    try:
        data = json.loads(request.body.decode(ENCODING))
    except ValueError as e:
        try:
            data = json.loads(request.body.decode(FALLBACKENCODING))
        except ValueError as e:
            return HttpResponseBadRequest(ERROR_JSON.format(e))
    try:
        title = data['title']
    except KeyError as e:
        title = None
    try:
        comment = data['comment']
    except KeyError as e:
        comment = None

    if not (title or comment):
        return HttpResponseBadRequest(ERROR_KEY.format('title and/or comment'))

    video = get_object_or_404(Video, source=video_url)

    if title:
        video.title = title
    if comment:
        video.comment = comment
    video.save()

    return HttpResponse()

def delete_photo(request, photo_url):
    """Delete a photo"""

    photo = get_object_or_404(Photo, source=photo_url)
    photo.delete()

    return HttpResponse()

def delete_video(request, video_url):
    """Delete a video"""

    video = get_object_or_404(Video, source=video_url)
    video.delete()

    return HttpResponse()

@require_http_methods(['GET'])
def view_album(request, album_url):
    """View an existing photo album in a web browser"""

    album = get_object_or_404(Album, album_url=album_url)

    return render(request, 'index.html', {
        'game_name': album.game_name,
        'items': album.photos.all(),
        })

@require_http_methods(['GET'])
def view_videos(request, album_url):
    """View an existing video album in a web browser"""

    album = get_object_or_404(Album, album_url=album_url)

    return render(request, 'videos.html', {
        'game_name': album.game_name,
        'items': album.videos.all(),
        })

@require_http_methods(['GET'])
def download_as_zip(request, album_url):
    """Download the photos of an album as a zipfile"""
    album = get_object_or_404(Album, album_url=album_url)
    photos = album.photos.all()

    # Use an bytestream rather than a real file
    temp_file = io.BytesIO()

    # Add photos to the zipfile
    with zipfile.ZipFile(temp_file, mode='w', compression=zipfile.ZIP_DEFLATED) as zip_file:
        for number, photo in enumerate(photos):
            path = os.path.join(settings.MEDIA_ROOT, photo.source.name)
            name = str(number+1)
            #name += ' - {}.jpg'.format(photo.comment) if photo.comment else '.jpg'
            name += '.jpg'
            zip_file.write(path, name)

    # Serve the contents of the zipfile
    file_size = temp_file.tell()
    temp_file.seek(0)
    response = HttpResponse(temp_file.getvalue(), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="{}.zip"'.format(album.game_name)
    response['Content-Length'] = file_size
    return response
