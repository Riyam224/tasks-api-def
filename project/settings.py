import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

# Load environment variables
load_dotenv()

# ========================
# Paths
# ========================
BASE_DIR = Path(__file__).resolve().parent.parent

# ========================
# Security
# ========================
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "fallback-secret-key")

# Debug: default False for safety
DEBUG = os.getenv("DEBUG", "False").lower() == "true"

# Allowed hosts (add your custom domain if you have one)
ALLOWED_HOSTS = [
    "web-production-3a3f2.up.railway.app",  # Railway domain
    "127.0.0.1",  # local dev
    "localhost",
]

# ========================
# Installed apps
# ========================
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party
    "drf_spectacular",
    "rest_framework",
    "corsheaders",
    # Local apps
    "tasks",
]


REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}


SPECTACULAR_SETTINGS = {
    "TITLE": "🚀 Tasks API",
    "DESCRIPTION": "A modern, simple API for managing tasks",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
}
# ========================
# Middleware
# ========================
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ========================
# URL & WSGI
# ========================
ROOT_URLCONF = "project.urls"
WSGI_APPLICATION = "project.wsgi.application"

# ========================
# Templates
# ========================
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

# ========================
# Database
# ========================
if os.getenv("DATABASE_URL"):
    # Railway Postgres
    DATABASES = {
        "default": dj_database_url.config(
            default=os.environ.get("DATABASE_URL"),
            conn_max_age=600,
            ssl_require=True,
        )
    }
else:
    # Local Postgres
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": os.getenv("POSTGRES_DB", "tasks_db"),
            "USER": os.getenv("POSTGRES_USER", "tasks_user"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD", "1234"),
            "HOST": os.getenv("POSTGRES_HOST", "localhost"),
            "PORT": os.getenv("POSTGRES_PORT", "5432"),
        }
    }

# ========================
# Password validation
# ========================
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ========================
# Internationalization
# ========================
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ========================
# Static & Media files
# ========================
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# ========================
# Default primary key
# ========================
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ========================
# CORS
# ========================
# In production, restrict to your frontend domain(s)
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True
else:
    CORS_ALLOWED_ORIGINS = [
        "https://your-frontend-domain.com",  # e.g. React/Flutter Web app
    ]

# ========================
# API Keys
# ========================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
