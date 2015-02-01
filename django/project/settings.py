'''
Django settings for photoserver project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
'''

import os
from django.core.exceptions import ImproperlyConfigured

# Set debug to false unless running locally
try:
    from project.debug_settings import DEBUG
except ImportError:
    DEBUG = False

# Import secret key from secret_settings.py
try:
    from project.secret_settings import SECRET_KEY
except ImportError:
    raise ImproperlyConfigured("Please specify a value for the variable SECRET_KEY in project/secret_settings.py. Make sure to never commit this file to any public repository!")

# Basic config variables
BASE_DIR         = os.path.dirname(os.path.dirname(__file__))
TEMPLATE_DEBUG   = DEBUG
ALLOWED_HOSTS    = ['localhost', 'photoserver.created.today']
ROOT_URLCONF     = 'project.urls'
WSGI_APPLICATION = 'project.wsgi.application'
STATIC_ROOT      = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'files'),)
STATIC_URL       = '/static/'
MEDIA_ROOT       = '/srv/photoserver'
MEDIA_URL        = '/photos/'
TEMPLATE_DIRS    = [os.path.join(BASE_DIR, 'templates')]
LANGUAGE_CODE    = 'en-us'
TIME_ZONE        = 'UTC'
USE_I18N         = False
USE_L10N         = False
USE_TZ           = True

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'photoserver',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
