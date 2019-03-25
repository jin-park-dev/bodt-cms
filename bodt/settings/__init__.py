from decouple import config, UndefinedValueError

try:
    ENV_IS_FOR = config('ENV_IS_FOR')

    if ENV_IS_FOR == 'local':
        print('Local Development setting is used')
        from .dev import *
    elif ENV_IS_FOR == 'production':
        print('Production Setting is used.')
        from .production import *
    else:
        print('No settings is found. Please check if .env exist')
except UndefinedValueError:
    print('CI setting is used. Maybe there is a error.')
    # from .ci import *
