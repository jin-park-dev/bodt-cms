from .base import *
from decouple import config

ENV_IS_FOR = config('ENV_IS_FOR')

if ENV_IS_FOR == 'local':

    DEBUG = True

    INSTALLED_APPS += [
        'django_extensions',
        'debug_toolbar',
    ]

    MIDDLEWARE += [
        'debug_toolbar.middleware.DebugToolbarMiddleware',
        'livereload.middleware.LiveReloadScript',
    ]

    # EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    INTERNAL_IPS = ["127.0.0.1", "localhost"]

    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'http')
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False

    SENDGRID_SANDBOX_MODE_IN_DEBUG=True
    SENDGRID_ECHO_TO_STDOUT=True

    GA_KEY_FILEPATH = 'wagtail-237316-364e043ba940.json'
    GA_VIEW_ID = 'ga:191694086'
