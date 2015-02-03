from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

@login_required
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

    #TODO: Implement this view
    pass;

@login_required
@require_http_methods(['POST'])
def create_photo(request):
    '''
    Create Photo POST /photo/
    ====================
    Input:
    ------
    - string albumId
    - string name of the photo
    - string comment on the photo
    - the jpg data itself, typically 640x400 so approx. 100 kByte.
    Returns: { photoId:.., photoUrl:..}
    --------
    - photoId: The photoId
    - photoUrl: The full URL of the full sized photo picture in the album
    '''

    #TODO: Implement this view
    pass;

@login_required
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
def view_album(request, album_id):
    '''
    Viewer page (URL from create Album above)
    =========================================
    HTTP GET URL (e.g. http://albums.elibom.nl/album/<difficult to guess albumID>

    - Shows overview of all photo’s in the album.
    - Clicking a photo shows the photo with next/prev
    - Shows comment of the photo
    - Download all photo’s in a ZIP (typically 4 Mbyte, Max 20 Mbyte)
    '''

    #TODO: Implement this view
    pass;
