from pathlib import Path
import os
import environ
from dotenv import load_dotenv
import os

from dotenv import load_dotenv
path = '.env'  #try .path[0] if 1 doesn't work
load_dotenv(path)

# env = environ.Env()
# environ.Env.read_env()
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("SECRET_KEY_FD")
DEBUG = os.environ['DEBUG'] == 'True'

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "storages",
    "main",
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

ROOT_URLCONF = 'drive.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR , 'templates'),
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

WSGI_APPLICATION = 'drive.wsgi.application'


DATABASES = {
    'default': {
        #  'ENGINE': 'django.db.backends.postgresql_psycopg2',
         'ENGINE': "django.db.backends.postgresql",
         'NAME': os.getenv('DB_NAME_FD'),
         'USER': os.getenv('DB_USER_HOST_FD'),
         'PASSWORD': os.getenv('DB_PASSWORD_HOST_FD'),
         'HOST': os.getenv("DB_HOST_FD"),
         'PORT': '5432',
    },
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

##############################    AWS    ##############################
# os.environ.setdefault('S3_USE_SIGV4', 'True')
USE_S3 = os.getenv('USE_S3') == 'True'
if USE_S3:
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID_FD2')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY_FD2')
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME_FD')

    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

    AWS_S3_FILE_OVERWRITE = False

    AWS_S3_REGION_NAME = "us-east-2"
    AWS_S3_SIGNATURE_VERSION = "s3v4"

    AWS_LOCATION = 'static'
    S3_URL = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME
    STATIC_URL = f'https://{S3_URL}/{AWS_LOCATION}/'


    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    AWS_S3_ENDPOINT_URL = "https://s3.us-east-2.amazonaws.com"
    #NEW
    # AWS_URL = os.getenv("AWS_URL_FD")
    
else:
    STATIC_URL = '/staticfiles/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')


# STORAGES = {
#     "default": {
#         "BACKEND": "storages.backends.s3.S3Storage",
#         "OPTIONS": {
#             "AWS_ACCESS_KEY_ID":AWS_ACCESS_KEY_ID,
#             "AWS_SECRET_ACCESS_KEY":AWS_SECRET_ACCESS_KEY,
#             "AWS_STORAGE_BUCKET_NAME":AWS_STORAGE_BUCKET_NAME,
#             "STATIC_URL":STATIC_URL,
#             "DEFAULT_FILE_STORAGE":'storages.backends.s3boto3.S3Boto3Storage',
#             "STATICFILES_STORAGE":'storages.backends.s3boto3.S3Boto3Storage',
#             "AWS_S3_FILE_OVERWRITE":False,
#             "AWS_S3_REGION_NAME":"us-east-2",
#             "AWS_S3_SIGNATURE_VERSION":"s3v4",
#             "AWS_S3_ENDPOINT_URL":"https://s3.us-east-2.amazonaws.com"
#             # "AWS_S3_ADDRESSING_STYLE":"virtual"
#         },
#     },
#     "staticfiles": {
#         "BACKEND": "storages.backends.s3.S3Storage",
#         "OPTIONS":{
#         }
#     },
# }