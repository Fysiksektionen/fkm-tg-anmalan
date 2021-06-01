import os
from pathlib import Path

from django.urls import reverse_lazy
from django.utils.log import DEFAULT_LOGGING

from .local import *


PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

with open(SECRET_KEY_PATH) as f:
    SECRET_KEY = f.read().strip()


DEBUG = False
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

ADMINS = [('admin', 'webmaster@f.kth.se')]
MANAGERS = ADMINS

# Application definition

ROOT_URLCONF = 'project_administration.urls'
WSGI_APPLICATION = 'project_administration.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'fkm_tg_anmalan',
    'django.contrib.admin'
)

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

# Templates
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [PROJECT_ROOT / 'venv/lib/python3.8/site-packages/'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASSWORD,
        'HOST': DB_HOST,
        'PORT': DB_PORT
    }
}

# Internationalization
LANGUAGE_CODE = 'sv'
TIME_ZONE = 'Europe/Stockholm'
USE_I18N = True
USE_L10N = True
USE_TZ = True
FIRST_DAY_OF_WEEK = 1

LOCALE_PATHS = [
    PROJECT_ROOT / 'locale',
]

AUTH_USER_MODEL = 'fkm_tg_anmalan.TGUser'

# Static files (CSS, JavaScript, Images)
STATIC_URL = ROOT_URL + '/public/staticfiles/'
STATIC_ROOT = PUBLIC_ROOT / 'staticfiles'
STATICFILES_DIRS = [
    PROJECT_ROOT / 'static',
]

MEDIA_URL = ROOT_URL + '/public/mediafiles/'
MEDIA_ROOT = PUBLIC_ROOT / 'mediafiles'
MEDIAFILES_DIRS = [
    PROJECT_ROOT / 'media',
]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Crispy settings
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Assure that errors end up to Apache error logs via console output
# when debug mode is disabled
DEFAULT_LOGGING['handlers']['console']['filters'] = []
# Enable logging to console from our modules by configuring the root logger
DEFAULT_LOGGING['loggers'][''] = {
    'handlers': ['console'],
    'level': 'INFO',
    'propagate': True
}


# Room settings
ROOM_MAX = 7
ROOM_NAMES = [
    "Plommonstopet",
    "Baskern",
    "Den trekantiga",
    "Cowboyhatten",
    "Fedoran",
    "The Force-kepsen",
    "Fezen",
    "El Sombrero",
    "Hattarna",
    "Mössorna"
]
