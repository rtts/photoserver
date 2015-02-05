import base64
from functools import wraps
from django.http import HttpResponse
from django.contrib.auth import authenticate, login

def http_auth(view, request, realm='', *args, **kwargs):
    """
    This code was kindly provided by StackOverflow user "Humphrey" at
    http://stackoverflow.com/questions/6068674/django-test-client-http-basic-auth-for-post-request/6118134#6118134
    """
    if 'HTTP_AUTHORIZATION' in request.META:
        auth = request.META['HTTP_AUTHORIZATION'].split()
        if len(auth) == 2:
            if auth[0].lower() == 'basic':
                uname, passwd = base64.b64decode(auth[1]).decode('utf-8').split(':')
                user = authenticate(username=uname, password=passwd)
                if user is not None and user.is_active:
                    login(request, user)
                    request.user = user
                    return view(request, *args, **kwargs)

    # When the authorization failed:
    response = HttpResponse('Failed')
    response.status_code = 401
    response['WWW-Authenticate'] = 'Basic realm="%s"' % realm
    return response

def http_auth_required(realm=''):
    """Decorator that requires HTTP Basic authentication, eg API views."""
    def view_decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            return http_auth(func, request, realm, *args, **kwargs)
        return wrapper
    return view_decorator
