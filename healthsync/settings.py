"""
Django settings for healthsync project.

Generated by 'django-admin startproject' using Django 5.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv() 
from decouple import config
import os
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'users.apps.UsersConfig',
    
    'captcha',
    
    'csp',
    
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'users.middleware.SessionExpiryMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'healthsync.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
                BASE_DIR / 'templates',
            ],
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

WSGI_APPLICATION = 'healthsync.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),           # The name of your PostgreSQL database
        'USER': os.getenv('DB_USER'),            # Your PostgreSQL username
        'PASSWORD': os.getenv('DB_PASSWORD'),       # Your PostgreSQL password
        'HOST': 'localhost',               # Use 'localhost' if PostgreSQL is on the same machine
        'PORT': '5432',                    # The default PostgreSQL port
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


#email config
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

MEDIA_URL = '/media/'
MEDIA_ROOT = 'media/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

RECAPTCHA_PUBLIC_KEY = os.getenv('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = os.getenv('RECAPTCHA_PRIVATE_KEY')

SESSION_COOKIE_AGE = 9000  # Set the session expiry to 15 minutes

LOGIN_URL = '/login/'  # URL of your login view
LOGOUT_REDIRECT_URL = '/login/'  # Redirect to login page after logout

# SESSION_EXPIRE_AT_BROWSER_CLOSE = True

SECRET_KEY_ENCRYPTION = config('SECRET_KEY_ENCRYPTION')


# Allow content from the same origin and specified external sources
CSP_DEFAULT_SRC = ("'self'",)  # Default policy for all content types

# Allow scripts from the same origin, Google APIs, jsDelivr, and Cloudflare
CSP_SCRIPT_SRC = (
    "'self'",
    "https://www.google.com",
    "https://maps.googleapis.com",
    "https://cdn.jsdelivr.net",
    "https://cdnjs.cloudflare.com",
)

# Allow styles from the same origin, Google Fonts, jsDelivr, and Cloudflare
CSP_STYLE_SRC = (
    "'self'",
    "https://fonts.googleapis.com",  # For Google Fonts
    "https://cdn.jsdelivr.net",
    "https://cdnjs.cloudflare.com",
)

# Allow images from the same origin, Google, and inline images (data URIs)
CSP_IMG_SRC = (
    "'self'",
    "https://www.google.com",
    "https://maps.googleapis.com",
    "data:",  # Allow inline images (data URIs)
)

# Allow fonts from the same origin and Google Fonts
CSP_FONT_SRC = (
    "'self'",
    "https://fonts.gstatic.com",
)

# Prevent embedding the site in frames, except from self
CSP_FRAME_ANCESTORS = ("'self'",)

# Allow connections (e.g., WebSockets) to these sources
CSP_CONNECT_SRC = (
    "'self'",
    "https://maps.googleapis.com",
    "https://cdn.jsdelivr.net",
    "https://cdnjs.cloudflare.com",
)




import os
import logging
import logging.config  # Import logging.config
from datetime import datetime

# Define the logs directory
LOG_DIR = os.path.join(BASE_DIR, 'logs')

# Create the logs directory if it doesn't exist
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Path for the main log file
LOG_FILE = os.path.join(LOG_DIR, 'activity.log')

# Custom handler to limit the number of lines
class LineLimitHandler(logging.FileHandler):
    def __init__(self, *args, max_lines=100, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_lines = max_lines
        self.line_count = self._get_line_count()

    def _get_line_count(self):
        if os.path.exists(self.baseFilename):
            with open(self.baseFilename, 'r') as f:
                return sum(1 for _ in f)
        return 0

    def emit(self, record):
        if self.line_count >= self.max_lines:
            self._rollover()
        super().emit(record)
        self.line_count += 1

    def _rollover(self):
        self.close()  # Close current log file
        new_file = f"{self.baseFilename}.{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
        os.rename(self.baseFilename, new_file)  # Rename the old log file
        self.line_count = 0  # Reset line count
        self.stream = self._open()  # Open new log file

# LOGGING configuration for Django
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'detailed': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(module)s - %(funcName)s - %(lineno)d',
        },
        'simple': {
            'format': '%(levelname)s %(message)s',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': LineLimitHandler,  # Use custom line limit handler
            'filename': LOG_FILE,
            'max_lines': 100,  # Set max lines before rollover
            'formatter': 'detailed',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
        'myapp': {  # Replace with your app name
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

# Add logging configuration
logging.config.dictConfig(LOGGING)  # Ensure logging configuration is applied
