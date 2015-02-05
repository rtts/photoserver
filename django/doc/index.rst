Photo Server API documentation
========================================

Photo Server provides a simple and reliable API for uploading photos
and viewing them in an album. The Django Admin interface (located at
`/admin/ </admin/>`_) provides an easy way to manage users,
permissions, and photo albums. Additionally, the Photo Server provides
a number of API calls that are documented on this page.

All requests that potentially modify data must include `HTTP Basic
access authentication <https://en.wikipedia.org/wiki/Basic_access_authentication>`_
credentials, by adding the HTTP header ``Authorization:`` following by
the string ``Basic`` and a base64-encoded ``username:password``
string. The users can be managed through the admin interface.

Creating and viewing albums
---------------------------

.. http:post:: /album/

   Create a new photo album

   **Example request**:

   .. sourcecode:: http

      POST /album/ HTTP/1.1
      Host: example.com
      Authorization: Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ==
      Content-Type: application/json

      {
        "gameName": "Erfenis - Fam. van Damme",
        "partnerName": "uitjes",
        "gameId": "870"
      }

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: application/json

      {
        "albumUrl": "aSL9LEu68tAPQWVb8yx0gf4XfHqaOINa",
        "albumId": "uitjes870"
      }

   :statuscode 200: The album has been successfully created and can
                    be accessed at /album/<albumUrl>/

   :statuscode 400: The request was either malformed or didn't contain
                    the correct JSON keys. The exact error is included
                    in the body of the response.

   :statuscode 409: The album already exists. The request body includes
                    the JSON keys `albumId` and `albumUrl` just like a
                    200 response

----------------------------------------------------------------------

.. http:get:: /album/<albumUrl>/

   View an existing photo album in a web browser

   .. NOTE::
      This API call does not require authentication.

   **Example request**:

   .. sourcecode:: http

      GET /album/aSL9LEu68tAPQWVb8yx0gf4XfHqaOINa/ HTTP/1.1
      Host: example.com

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: text/html; charset=utf-8

      <!doctype html>
      ...

Creating, updating, and deleting photos
---------------------------------------

.. http:post:: /photo/

   Add a new photo to an album

   **Example request**:

   .. sourcecode:: http

      POST /photo/ HTTP/1.1
      Host: example.com
      Authorization: Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ==
      Content-Type: application/json

      {
        "albumId": "uitjes870",
        "jpgData": "/9j/4AAQSkZJRgABAQEASABIAAD//gATQ3JlYXRlZCB3aXRoIEdJTVD/2wBDAP//////////////////////////////////////////////////////////////////////////////////////2wBDAf//////////////////////////////////////////////////////////////////////////////////////wgARCAAKAAoDAREAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAH/xAAWAQEBAQAAAAAAAAAAAAAAAAAAAQL/2gAMAwEAAhADEAAAAZNAg//EABQQAQAAAAAAAAAAAAAAAAAAACD/2gAIAQEAAQUCH//EABQRAQAAAAAAAAAAAAAAAAAAACD/2gAIAQMBAT8BH//EABQRAQAAAAAAAAAAAAAAAAAAACD/2gAIAQIBAT8BH//EABQQAQAAAAAAAAAAAAAAAAAAACD/2gAIAQEABj8CH//EABQQAQAAAAAAAAAAAAAAAAAAACD/2gAIAQEAAT8hH//aAAwDAQACAAMAAAAQ2/8A/8QAFBEBAAAAAAAAAAAAAAAAAAAAIP/aAAgBAwEBPxAf/8QAFBEBAAAAAAAAAAAAAAAAAAAAIP/aAAgBAgEBPxAf/8QAFBABAAAAAAAAAAAAAAAAAAAAIP/aAAgBAQABPxAf/9k="
      }

   .. NOTE::
      The request may optionally contain the key "comment", which
      will be saved along with the photo.

   .. NOTE::
      The submitted JPG data will be verified to contain a valid image.

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: application/json

      {
        "photoUrl": "/uitjes870/e4mqPHxtvwzSmXfSzz8r3mj0HrWQM8Or.jpg",
      }

   :statuscode 200: The photo has been successfully created and can
                    be accessed at /photo/<photoUrl>/

   :statuscode 400: The request was either malformed or didn't contain
                    the correct JSON keys. The exact error is included
                    in the body of the response.

----------------------------------------------------------------------

.. http:put:: /photo/<photoUrl>/

   Update the comment on an existing photo

   **Example request**:

   .. sourcecode:: http

      PUT /photo/uitjes870/e4mqPHxtvwzSmXfSzz8r3mj0HrWQM8Or.jpg HTTP/1.1
      Host: example.com
      Authorization: Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ==
      Content-Type: application/json

      {
        "comment": "Two kittens on an air mattress approaching a waterfall"
      }

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK

   :statuscode 200: The photo was successfully updated with the new
                    comment.

   :statuscode 400: The request was either malformed or didn't contain
                    the correct JSON keys. The exact error is included
                    in the body of the response.

   :statuscode 404: The photo could not be found.

----------------------------------------------------------------------

.. http:delete:: /photo/<photoUrl>/

   Delete a photo

   **Example request**:

   .. sourcecode:: http

      DELETE /photo/uitjes870/e4mqPHxtvwzSmXfSzz8r3mj0HrWQM8Or.jpg HTTP/1.1
      Host: example.com
      Authorization: Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ==

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK

   :statuscode 200: The photo was successfully deleted.

   :statuscode 404: The photo could not be found.