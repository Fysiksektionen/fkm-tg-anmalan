import json
import os

from django.urls import reverse_lazy
from django.utils.log import DEFAULT_LOGGING

def join_urls(*args):
    for arg in args:
        if not isinstance(arg, str):
            raise TypeError("Argument %s is not a string" % str(arg))

    if len(args) > 0:
        path = '/'.join([arg.strip('/') for arg in args])
        if len(args[0]) > 0 and args[0][0] == '/' and path[0] != '/':
            path = '/' + path

        if len(args) > 1:
            if len(args[-1]) > 0 and args[-1][-1] == '/' and path[-1] != '/':
                path = path + '/'
        else:
            if len(args[-1]) > 1 and args[-1][-1] == '/' and path[-1] != '/':
                path = path + '/'
    return path

def read_conf_json_settings(filepath):
    with open(filepath) as file:
        return json.load(file)


PROJECT_APP_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
PROJECT_ROOT = PROJECT_APP_ROOT
PUBLIC_ROOT = os.path.abspath(os.path.join(PROJECT_ROOT, 'public'))

file_settings = read_conf_json_settings(os.path.join(os.path.dirname(__file__), 'config_files/settings.json'))
ROOT_URL = file_settings.get('ROOT_URL')
DOMAIN_URL = file_settings.get('DOMAIN_URL')
if DOMAIN_URL and len(DOMAIN_URL) > 0 and DOMAIN_URL[-1] == '/':
    DOMAIN_URL = DOMAIN_URL[:-1]
SECRET_KEY_PATH = file_settings.get('SECRET_KEY_PATH')
with open(SECRET_KEY_PATH) as f:
    SECRET_KEY = f.read().strip()

DEBUG = False
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

ALLOWED_HOSTS = (
    'localhost',
    '0.0.0.0',
    'f.kth.se'
)

ADMINS = [('admin', 'ejemyr@fysiksektionen.se')]
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
        'DIRS': [os.path.join(PROJECT_ROOT, 'venv/lib/python3.8/site-packages/')],
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
                #'nollesystemet.context_processors.site_settings'
            ],
        },
    },
]

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'OPTIONS': {
            'read_default_file': os.path.join(os.path.dirname(__file__), 'config_files/db_info.cnf'),
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
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
    os.path.join(PROJECT_ROOT, 'locale'),
]

AUTH_USER_MODEL = 'fkm_tg_anmalan.TGUser'

# Static files (CSS, JavaScript, Images)
STATIC_URL = join_urls(ROOT_URL, '/staticfiles/')
STATIC_ROOT = os.path.join(PUBLIC_ROOT, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, 'static'),
]

MEDIA_URL = join_urls(ROOT_URL, '/mediafiles/')
MEDIA_ROOT = os.path.join(PUBLIC_ROOT, 'mediafiles')
MEDIAFILES_DIRS = [
    os.path.join(PROJECT_ROOT, 'media'),
]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Crispy settings
CRISPY_TEMPLATE_PACK = 'bootstrap4'


# Email setup
email_settings = read_conf_json_settings(os.path.join(os.path.dirname(__file__), 'config_files/mail.json'))
EMAIL_BACKEND = email_settings.get('EMAIL_BACKEND')
EMAIL_HOST = email_settings.get('EMAIL_HOST')
EMAIL_USE_TLS = email_settings.get('EMAIL_USE_TLS')
EMAIL_PORT = email_settings.get('EMAIL_PORT')
EMAIL_HOST_USER = email_settings.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = email_settings.get('EMAIL_HOST_PASSWORD')
DEFAULT_FROM_EMAIL = email_settings.get('DEFAULT_FROM_EMAIL')
SERVER_EMAIL = email_settings.get('SERVER_EMAIL')

# Assure that errors end up to Apache error logs via console output
# when debug mode is disabled
DEFAULT_LOGGING['handlers']['console']['filters'] = []
# Enable logging to console from our modules by configuring the root logger
DEFAULT_LOGGING['loggers'][''] = {
    'handlers': ['console'],
    'level': 'INFO',
    'propagate': True
}

room_settings = read_conf_json_settings(os.path.join(os.path.dirname(__file__), 'config_files/room_settings.json'))
ROOM_MAX = room_settings['max_count']
ROOM_NAMES = room_settings['names']

