

from pathlib import Path
import os
import sys
from dotenv import load_dotenv
from datetime import timedelta
import dj_database_url

# Load environment variables from .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ======================================
# CORE DJANGO SETTINGS (COMMON TO BOTH)
# ======================================

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-&h2+ej0l*v#-ji_hf9zlzj7xtyi!2+)c*e+3o_)bkkg(@p35ed')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '192.168.173.33']

# Application definition
INSTALLED_APPS = [
    # Django core apps (MUST BE IN THIS ORDER)
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'django_extensions',
    
    # Local apps
    'accounts',
    'core',
    'chat',
    
    # Channels (must be after regular apps)
    'channels',
    'daphne',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'accounts.middleware.RefreshOnExpiredMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'chatterly.urls'

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

WSGI_APPLICATION = 'chatterly.wsgi.application'
ASGI_APPLICATION = 'chatterly.asgi.application'

# Database
DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "chatterly",
        "USER": "jainil",
        "PASSWORD": "J@inil28082004",
        "HOST": "127.0.0.1",
        "PORT": "5432",
    }
}

# Redis (development)
REDIS_URL = 'redis://127.0.0.1:6379'

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL + "/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("localhost", 6379)],
        },
    },
}

# Password validation
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom user model
AUTH_USER_MODEL = 'accounts.CustomUser'

# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'accounts.authentication.CookieJWTAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# JWT Settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=45),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True').lower() == 'true'
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'paras0mani6@gmail.com')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'toih puho xmmi xpho')
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'paras0mani6@gmail.com')

# Cookie settings (for development)
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SAMESITE = 'Lax'

# ======================================
# PRODUCTION SETTINGS (RENDER.COM)
# ======================================
if 'RENDER' in os.environ:
    print("✅ Running in Render production environment")
    
    # Production security
    DEBUG = False
    
    # Update ALLOWED_HOSTS
    ALLOWED_HOSTS = [
        'chatterly-chat-application.onrender.com',
        'chatterly.onrender.com',
        '.onrender.com',
        'localhost',
        '127.0.0.1',
    ]
    
    # Production CSRF settings
    CSRF_TRUSTED_ORIGINS = [
        'https://chatterly-chat-application.onrender.com',
        'https://chatterly.onrender.com',
        'https://*.onrender.com',
    ]
    
    # Database - Use DATABASE_URL from environment
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL', 'postgresql://chatterly_chat_user:kuMqafAd4dfoeCoYwmR5NHSiAcUJvheA@dpg-d4q0h6khg0os73800dhg-a/chatterly_chat'),
            conn_max_age=600,
            ssl_require=True
        )
    }
    
    # Redis - Use REDIS_URL from environment
    REDIS_URL = os.environ.get('REDIS_URL', 'rediss://red-d4q0jteuk2gs73fe3ihg:6379')
    
    # Update cache configuration
    CACHES = {
        "default": {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": REDIS_URL + "/1",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                "CONNECTION_POOL_KWARGS": {"max_connections": 10},
            }
        }
    }
    
    # Update Channels layer
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "channels_redis.core.RedisChannelLayer",
            "CONFIG": {
                "hosts": [REDIS_URL],
                "capacity": 1500,
                "expiry": 10,
            },
        },
    }
    
    # Production security headers
    SECURE_SSL_REDIRECT = False
    SECURE_HSTS_SECONDS = 0
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False
    SECURE_BROWSER_XSS_FILTER = False
    SECURE_CONTENT_TYPE_NOSNIFF = False
    
    # Cookie settings for production (HTTPS)
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_SAMESITE = 'None'
    CSRF_COOKIE_SAMESITE = 'None'
    
    # Static files with WhiteNoise
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    
    print("✅ Production settings applied")
else:
    print("⚡ Running in local development environment")






# # ======================================
# # RENDER.COM PRODUCTION SETTINGS
# # ======================================
# import os
# import dj_database_url

# # Check if running on Render
# if 'RENDER' in os.environ:
#     print("✅ Running in Render production environment")
    
#     # Production security
#     DEBUG = False
    
#     # Update ALLOWED_HOSTS
#     ALLOWED_HOSTS = [
#         'chatterly-chat-application.onrender.com',
#         'chatterly.onrender.com',
#         '.onrender.com',
#         'localhost',
#         '127.0.0.1',
#     ]
    
#     # Production CSRF settings
#     CSRF_TRUSTED_ORIGINS = [
#         'chatterly-chat-application.onrender.com',
#         'https://chatterly.onrender.com',
#         'https://*.onrender.com',
#     ]
    
#     # Database - Use DATABASE_URL from environment
#     DATABASES = {
#         'default': dj_database_url.config(
#             default=os.environ.get('DATABASE_URL' , 'postgresql://chatterly_chat_user:kuMqafAd4dfoeCoYwmR5NHSiAcUJvheA@dpg-d4q0h6khg0os73800dhg-a/chatterly_chat'),
#             conn_max_age=600,
#             ssl_require=True
#         )
#     }
    
#     # Redis - Use REDIS_URL from environment
#     REDIS_URL = os.environ.get('REDIS_URL', 'redis://red-d4q0jteuk2gs73fe3ihg:6379')
    
#     # Update cache configuration
#     CACHES = {
#         "default": {
#             "BACKEND": "django_redis.cache.RedisCache",
#             "LOCATION": REDIS_URL + "/1",
#             "OPTIONS": {
#                 "CLIENT_CLASS": "django_redis.client.DefaultClient",
#                 "CONNECTION_POOL_KWARGS": {"max_connections": 10},  # Limit connections
#             }
#         }
#     }
    
#     # Update Channels layer
#     CHANNEL_LAYERS = {
#         "default": {
#             "BACKEND": "channels_redis.core.RedisChannelLayer",
#             "CONFIG": {
#                 "hosts": ['redis://red-d4q0jteuk2gs73fe3ihg:6379'],
#                 "capacity": 1500,  # Increase for production
#                 "expiry": 10,
#             },
#         },
#     }
    
#     # Production security headers
#     SECURE_SSL_REDIRECT = True
#     SECURE_HSTS_SECONDS = 31536000  # 1 year
#     SECURE_HSTS_INCLUDE_SUBDOMAINS = True
#     SECURE_HSTS_PRELOAD = True
#     SECURE_BROWSER_XSS_FILTER = True
#     SECURE_CONTENT_TYPE_NOSNIFF = True
    
#     # Cookie settings for production (HTTPS)
#     SESSION_COOKIE_SECURE = True
#     CSRF_COOKIE_SECURE = True
#     SESSION_COOKIE_SAMESITE = 'None'
#     CSRF_COOKIE_SAMESITE = 'None'
    
#     # Static files with WhiteNoise
#     STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    
#     # Email settings (already reading from .env)
#     EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    
#     print("✅ Production settings applied")
# else:
#     print("⚡ Running in local development environment")
#     # Your local development settings remain unchanged
    
#     from pathlib import Path
#     import os
#     from dotenv import load_dotenv
    
#     # Load environment variables from .env file
#     load_dotenv()
    
#     BASE_DIR = Path(__file__).resolve().parent.parent
    
#     # Get SECRET_KEY from environment variable (fallback to current key)
#     SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-&h2+ej0l*v#-ji_hf9zlzj7xtyi!2+)c*e+3o_)bkkg(@p35ed')
    
#     DEBUG = True
    
#     ALLOWED_HOSTS = ['chatterly-chat-application.onrender.com' , '127.0.0.1', 'localhost','192.168.173.33' , 'chatterly.onrender.com']
    
#     INSTALLED_APPS = [
#         'daphne',
#         'channels',
#         'django.contrib.admin',
#         'accounts',
#         'django.contrib.auth',
#         'django.contrib.contenttypes',
#         'django.contrib.sessions',
#         'django.contrib.messages',
#         'django.contrib.staticfiles',
#         'django_extensions',
#         'rest_framework',
#         'rest_framework_simplejwt',
#         'rest_framework_simplejwt.token_blacklist',
#         'core',
#         'chat',   
#     ]
    
#     MIDDLEWARE = [
#         'django.middleware.security.SecurityMiddleware',
#         "whitenoise.middleware.WhiteNoiseMiddleware",
#         'django.contrib.sessions.middleware.SessionMiddleware',
#         'accounts.middleware.RefreshOnExpiredMiddleware',
#         'django.middleware.common.CommonMiddleware',
#         'django.middleware.csrf.CsrfViewMiddleware',
#         'django.contrib.auth.middleware.AuthenticationMiddleware',
#         'accounts.middleware.RefreshOnExpiredMiddleware',
#         'django.contrib.messages.middleware.MessageMiddleware',
#         'django.middleware.clickjacking.XFrameOptionsMiddleware',
#     ]
    
#     ROOT_URLCONF = 'chatterly.urls'
    
#     TEMPLATES = [
#         {
#             'BACKEND': 'django.template.backends.django.DjangoTemplates',
#             'DIRS': [],
#             'APP_DIRS': True,
#             'OPTIONS': {
#                 'context_processors': [
#                     'django.contrib.auth.context_processors.auth',
#                     'django.template.context_processors.request',
#                     'django.contrib.messages.context_processors.messages',
#                 ],
#             },
#         },
#     ]
    
#     ASGI_APPLICATION = 'chatterly.asgi.application'
    
#     CACHES = {
#       "default": {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": "redis://127.0.0.1:6379/1",
#         "OPTIONS": {
#           "CLIENT_CLASS": "django_redis.client.DefaultClient",
#         }
#       }
#     }
    
#     CHANNEL_LAYERS = {
#       "default": {
#         "BACKEND": "channels_redis.core.RedisChannelLayer",
#         "CONFIG": {
#           "hosts": [("localhost", 6379)],
#         },
#       },
#     }
    
#     DATABASES = {
#         'default': {
#             "ENGINE": "django.db.backends.postgresql",
#             "NAME": "chatterly",
#             "USER": "jainil",
#             "PASSWORD": "J@inil28082004",
#             "HOST": "127.0.0.1",
#             "PORT": "5432",
#         }
#     }
    
#     AUTH_PASSWORD_VALIDATORS = [
#         {
#             'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
#         },
#         {
#             'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
#         },
#         {
#             'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
#         },
#         {
#             'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
#         },
#     ]
    
#     LANGUAGE_CODE = 'en-us'
#     TIME_ZONE = 'UTC'
#     USE_I18N = True
#     USE_TZ = True
    
#     STATIC_URL = 'static/'
#     STATIC_ROOT = BASE_DIR / "staticfiles"
#     STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
    
#     DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
#     AUTH_USER_MODEL = 'accounts.CustomUser'
    
#     REST_FRAMEWORK = {
#         'DEFAULT_AUTHENTICATION_CLASSES': [
#             'accounts.authentication.CookieJWTAuthentication',
#         ],
#         'DEFAULT_PERMISSION_CLASSES': [
#             'rest_framework.permissions.IsAuthenticated',
#         ],
#     }
    
#     AUTHENTICATION_BACKENDS = [
#         'django.contrib.auth.backends.ModelBackend',
#     ]
    
#     from datetime import timedelta
    
#     SIMPLE_JWT = {
#         'ACCESS_TOKEN_LIFETIME': timedelta(minutes=45),
#         'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
#         'ROTATE_REFRESH_TOKENS': True,
#         'BLACKLIST_AFTER_ROTATION': True,
#     }
    
#     # Email Configuration - Read from .env file
#     EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#     EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.gmail.com')
#     EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
#     EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True').lower() == 'true'
#     EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', 'paras0mani6@gmail.com')
#     EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', 'toih puho xmmi xpho')
#     DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', 'paras0mani6@gmail.com')
    
#     MEDIA_URL = '/media/'
#     MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    
#     SESSION_COOKIE_SECURE = True
#     CSRF_COOKIE_SECURE = True
#     SESSION_COOKIE_SAMESITE = 'None'
#     CSRF_COOKIE_SAMESITE = 'None'


