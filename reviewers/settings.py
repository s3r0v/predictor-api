"""
Django settings for reviewers project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
from telnetlib import AUTHENTICATION
from dotenv import dotenv_values

config = dotenv_values(".env")

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-l%tqhnayeasq6ah@g=kj5f&q%57@ac_szs)8b+s)6z@tq&(9bv'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    "rest_framework",
    "django_filters",
    "ckeditor",
    "ckeditor_uploader",
    'djoser',
    'rest_framework.authtoken',
    'django_q',
    'nested_admin',

    "news",
    "prediction",
    "tradesData",
]

MIDDLEWARE = [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'reviewers.urls'
CSRF_TRUSTED_ORIGINS = ['https://sea-lion-app-y7z7y.ondigitalocean.app']

CORS_ALLOWED_ORIGINS=[
    "https://127.0.0.1:8080",
    "https://0.0.0.0:8080",
    "https://sea-lion-app-y7z7y.ondigitalocean.app",
]

CORS_ALLOW_ALL_ORIGINS=True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'reviewers.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config["DB_NAME"],
        "USER": config["DB_USERNAME"],
        "PASSWORD": config["DB_PASSWORD"],
        "PORT": config["DB_PORT"],
        "HOST": config["DB_HOST"],
        "DISABLE_SERVER_SIDE_CURSORS": True,
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CKEDITOR_UPLOAD_PATH = "uploads/"

MINT_AUTHORITIES = ['2WB9oJV1se6xX1bfL67FWWKQfwtGTwSemWMFAJdVueEo']
BINANCE_API = 'https://testnet.binancefuture.com/fapi/v1/klines?'
SOLSCAN_API_HOLDERS = 'https://public-api.solscan.io/token/meta?tokenAddress='
SOLSCAN_API = 'https://api.solscan.io/account?address='
SOLSCAN_API_TOKENS = 'https://api.solscan.io/account/v2/tokens?address=DywvRGQzikkTfgakuh76WGKru7FWHX3HnFgS1CUGzGQt'
TOKEN_SYMBOL = 'Rev'
TOKEN_NAME = 'Reviewers #88'
CREATOR = 'DywvRGQzikkTfgakuh76WGKru7FWHX3HnFgS1CUGzGQt'