from pathlib import Path

# URLs
ROOT_URL = "/tg2"
DOMAIN_URL = ""

# Static files
PUBLIC_ROOT = Path(__file__).resolve().parent.parent.parent / 'public'

# Security
SECRET_KEY_PATH = ""
ALLOWED_HOSTS = ['']

# Database
DB_NAME = ''
DB_USER = ''
DB_PASSWORD = ''
DB_HOST = ''
DB_PORT = ''

# Email settings
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = ""
EMAIL_USE_TLS = True
EMAIL_PORT = 587
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
DEFAULT_FROM_EMAIL = ""
SERVER_EMAIL = DEFAULT_FROM_EMAIL
