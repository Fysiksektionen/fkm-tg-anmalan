from project_administration.settings.base import *

TMP_PATH = PROJECT_ROOT / 'tmp'

DEBUG = True
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

if 'debug_toolbar' not in INSTALLED_APPS:
    INSTALLED_APPS += ('debug_toolbar',)
    MIDDLEWARE = ('debug_toolbar.middleware.DebugToolbarMiddleware',) + MIDDLEWARE

ALLOWED_HOSTS = (
    '*'
)

