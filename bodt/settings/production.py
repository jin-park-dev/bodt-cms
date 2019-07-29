from .base import *
from decouple import config

ENV_IS_FOR = config('ENV_IS_FOR')

if ENV_IS_FOR == 'production':
    DEBUG = False
    # EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

    EMAIL_HOST = 'smtp.sendgrid.net'
    EMAIL_HOST_USER = 'yourusername@youremail.com'
    EMAIL_HOST_PASSWORD = 'your password'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True

    SENDGRID_SANDBOX_MODE_IN_DEBUG=False
    SENDGRID_ECHO_TO_STDOUT=True
