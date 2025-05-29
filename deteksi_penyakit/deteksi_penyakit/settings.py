from pathlib import Path

# ======== BASE DIRECTORY ========
BASE_DIR = Path(__file__).resolve().parent.parent

# ======== SECURITY ========
SECRET_KEY = 'django-insecure-j(v5yu5!gt4z*9gb268_1s)(ye_=%#y+y6&lfkk2n)d7ph4&^5'
DEBUG = True
ALLOWED_HOSTS = []

# ======== APLIKASI YANG DIGUNAKAN ========
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'diagnosa',  # aplikasi utama kita
]

# ======== MIDDLEWARE ========
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ======== URLS & TEMPLATE ========
ROOT_URLCONF = 'deteksi_penyakit.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],  # ini sudah oke
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',  # penting untuk {% url %} dan login
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'deteksi_penyakit.wsgi.application'

# ======== DATABASE ========
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# ======== VALIDASI PASSWORD ========
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# ======== LOKALISASI ========
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ======== STATIC FILES ========
STATIC_URL = '/static/'

# ======== FIELD UTAMA DEFAULT ========
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ======== AUTENTIKASI LOGIN REDIRECT & URL LOGIN ========
LOGIN_REDIRECT_URL = '/'   # setelah login berhasil, redirect ke halaman utama
LOGIN_URL = '/login/'      # jika belum login, redirect ke halaman ini
LOGOUT_REDIRECT_URL = 'login'
