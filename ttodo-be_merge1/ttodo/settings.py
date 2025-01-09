from pathlib import Path
import os
import json
import sys

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# secrets.json 파일을 찾아줍니다.
SECRET_BASE_FILE = os.path.join(BASE_DIR, 'secrets.json')

# secrets.json 파일을 읽고, json key/value 값들을 secrets에 할당합니다.
secrets = json.load(open(SECRET_BASE_FILE))

# SECRET_KEY를 명시적으로 설정
SECRET_KEY = secrets["SECRET_KEY"]

# 나머지 설정들을 동적으로 할당
for key, value in secrets.items():
    if key != "SECRET_KEY":  # SECRET_KEY는 이미 설정했으므로 제외
        setattr(sys.modules[__name__], key, value)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']


# Application definition

INSTALLED_APPS = [
    'accounts',
    'mypage',
    'boards',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites', 
    # DRF
    'rest_framework',
    # dj_rest_auth 를 사용하려면 아래 app이 선행되어야 한다.
    'rest_framework.authtoken',
    
    # Social 로그인을 위한 app
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    
    # Naver
    'allauth.socialaccount.providers.naver',
    'allauth.socialaccount.providers.kakao',
    
    # dj_rest_auth
    'dj_rest_auth',
    'dj_rest_auth.registration',
    
    # token
    'rest_framework_simplejwt',
    'corsheaders',
]

AUTH_USER_MODEL = 'accounts.User' #추가!! 없으면 오류 발생 "앱이름.모델명" user모델생성 후 allauth말고 내가 생성한 모델을 우선으로 적용
 
SITE_ID = 1 #추가



MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware', # 추가
]


CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'ttodo.urls'

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

WSGI_APPLICATION = 'ttodo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
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


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


from datetime import timedelta


# rest framework 에 대한 설정
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    # 기본 인증에 대한 설정
    'DEFAULT_AUTHENTICATION_CLASSES': (
        # dj_rest_auth 의 인증 절차 중 JWTCookieAuthentication을 사용
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'dj_rest_auth.jwt_auth.JWTCookieAuthentication',
    ),
    # 허가에 대한 설정
    'DEFAULT_PERMISSION_CLASSES': (
    	# 인증이 완료된 사용자에 한해서 접근 허가
        'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.AllowAny',
    )
}

# cookie key 와 refresh cookie key 의 이름을 설정
JWT_AUTH_COOKIE = 'sociallogin-auth'
JWT_AUTH_REFRESH_COOKIE = 'sociallogin-refresh-token'

# JWT 사용을 위한 설정
REST_USE_JWT = True

# simplejwt 에 대한 설정
SIMPLE_JWT = {
    # access token 의 유효기간
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    # refresh token 의 유효기간
    'REFRESH_TOKEN_LIFETIME': timedelta(days=2),
    # 토큰에 들어갈 알고리즘
    'ALGORITHM': 'HS256',
    # 토큰을 만드는데 사용할 secret key
    'SIGNING_KEY': SECRET_KEY,
}

# MEDIA_URL = '/media/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

LOGIN_REDIRECT_URL = 'mypage:mypage'  # 'home'은 로그인 후 리다이렉트할 URL의 name입니다.

MAIN_DOMAIN = 'http://127.0.0.1:8000/'

SOCIALACCOUNT_STORE_TOKENS = True

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
CSRF_TRUSTED_ORIGINS = ['http://localhost:3000', "http://127.0.0.1:3000",]
CORS_ORIGIN_WHITELIST = ['http://localhost:3000', "http://127.0.0.1:3000",]

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    # 'x-CSRFToken',
    'csrftoken'
    'x-requested-with',
]

