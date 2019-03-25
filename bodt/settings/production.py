from .base import *
from decouple import config

ENV_IS_FOR = config('ENV_IS_FOR')

if ENV_IS_FOR == 'production':
    DEBUG = False
