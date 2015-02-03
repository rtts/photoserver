import json
import base64
from django.shortcuts import render, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.base import ContentFile
from .utils import http_auth_required
from .models import Album, Photo

HTTP_AUTH_REALM = "Photoserver-API"
ERROR_JSON = 'You are sending invalid JSON! The exact error is: "{}"'
ERROR_KEY = 'The request doesn’t contain the required arguments. At least the following key is missing: {}'
ERROR_BASE64 = 'The Jpeg data couldn’t be decoded using base64. The exact error is: "{}"'
ERROR_JPG = 'The image you supplied is not a valid image. Is the Jpeg data corrupted?'

@csrf_exempt
@http_auth_required(realm=HTTP_AUTH_REALM)
@require_http_methods(['POST'])
def create_album(request):
    '''
    Create album POST /album/
    ============

    Input: {gameName:.., partnerName:.. gameId:..}
    ------
    - string gameName e.g. "erfenis -  Fam. van Damme", used for the title of the album
    - string partnerName e.g. "uitjes", used to generate unique id
    - String gameId bijv "870", could be used with previous field to generate unique id

    Returns: {albumId:.., albumUrl:..}
    --------
    - String albumId: identifier of this album
    - String albumUrl: URL of the album, including some generated password so that only people with the link can see the album using a browser

    Status code:
    -------
    200 OK
    '''

    try:
        data = json.loads(request.body.decode('utf-8'))
    except ValueError as e:
        return HttpResponseBadRequest(ERROR_JSON.format(e))

    try:
        album = Album(
            game_name = data['gameName'],
            partner_name = data['partnerName'],
            game_id = data['gameId'],
        )
    except KeyError as e:
        return HttpResponseBadRequest(ERROR_KEY.format(e))

    album.save()
    return JsonResponse({
        'albumId': album.album_id,
        'albumUrl': album.album_url,
        })

@csrf_exempt
@http_auth_required(realm=HTTP_AUTH_REALM)
@require_http_methods(['POST'])
def create_photo(request):
    '''
    Create Photo POST /photo/
    ====================
    Input:
    ------
    - string albumId
    - string comment (optional)
    - base64 encoded string jpgData

    Returns: { photoId:.., photoUrl:..}
    --------
    - photoUrl: The full URL of the full sized photo picture in the album
    '''

    # Cautiously extract and decode request data
    try:
        data = json.loads(request.body.decode('utf-8'))
    except ValueError as e:
        return HttpResponseBadRequest(ERROR_JSON.format(e))
    try:
        album = get_object_or_404(Album, album_id=data['albumId'])
        encoded_jpg = data['jpgData']
    except KeyError as e:
        return HttpResponseBadRequest(ERROR_KEY.format(e))
    try:
        decoded_jpg = base64.b64decode(data['jpgData'], validate=True)
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
        'photoUrl': photo.source.url,
        })

@csrf_exempt
@http_auth_required(realm=HTTP_AUTH_REALM)
@require_http_methods(['PUT', 'DELETE'])
def update_delete_photo(request, album_id, photo_id):
    if request.method == 'PUT':
        return update_photo(request, album_id, photo_id)
    elif request.method == 'DELETE':
        return delete_photo(request, album_id, photo_id)

def update_photo(request, album_id, photo_id):
    '''
    Change comment on photo (PUT album/<albumID>/photo/<photoId>
    =======================
    Input: { comment: .. }
    ------
    - photoId from the PUT command
    - The new comment
    Returns:
    --------
    Status code
    '''
    #TODO: Implement this view
    pass;

def delete_photo(request, album_id, photo_id):
    '''
    Delete Photo DELETE album/<albumID>/photo/<photoID>
    ===================================================
    Input:
    ------
    Returns:
    --------
    Status code
    '''

    #TODO: Implement this view
    pass;

@require_http_methods(['GET'])
def view_album(request, album_url):
    '''
    Viewer page (URL from create Album above)
    =========================================
    HTTP GET URL (e.g. http://albums.elibom.nl/album/<difficult to guess albumID>

    - Shows overview of all photo’s in the album.
    - Clicking a photo shows the photo with next/prev
    - Shows comment of the photo
    - Download all photo’s in a ZIP (typically 4 Mbyte, Max 20 Mbyte)
    '''

    album = get_object_or_404(Album, album_url=album_url)
    return HttpResponse("You've requested the album " + str(album))











