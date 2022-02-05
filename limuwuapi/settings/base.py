

# THIS BASE.PY SETTINGS IS USED FOR LOCAL DEVELOPMENT PURPOSES 
# THE OTHER FILES IN THIS DIRECTORY (STAGING & PRODUCTION) WILL OVERWRITE SOME SETTINGS VARIABLES HERE


import os
from pathlib import Path
from dotenv import dotenv_values, load_dotenv

# Load dot env file based on each environment
if os.environ.get('DJANGO_SETTINGS_MODULE') == 'limuwuapi.settings.base':
    print("USING ENV VAR FROM ====> .env.dev file")
    load_dotenv(".env.dev")
    print("====== Activated Settings -> base.py (development / local)")

elif os.environ.get('DJANGO_SETTINGS_MODULE') == 'limuwuapi.settings.stag':
    print("USING ENV VAR FROM ====> .env.stag file")
    load_dotenv(".env.stag")
    print("====== Activated Settings -> stag.py (staging)")
    
elif os.environ.get('DJANGO_SETTINGS_MODULE') == 'limuwuapi.settings.prod':
    print("USING ENV VAR FROM ====> .env.prod file")
    load_dotenv(".env.prod")
    print("====== Activated Settings -> prod.py (production)")
else:
    print("No settings, exited")



BASE_DIR = Path(__file__).resolve().parent.parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY') # taruh di .env

DEBUG = bool(int(os.environ.get('DEBUG'))) # taruh di .env

ALLOWED_HOSTS = [] 


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'clients.apps.ClientsConfig',
    'core.apps.CoreConfig',

    'membership',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'limuwuapi.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'limuwuapi.wsgi.application'



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
    
} 



AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [
#    os.path.join(BASE_DIR, "static"),
   ]

# The code below, you can also use Path() instead of os.path.join()
MEDIA_ROOT = Path(BASE_DIR, 'media')
MEDIA_URL = '/media/'


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

