INSTALLED_APPS = [
    # ... الملفات الأساسية ...
    'rest_framework',
    'rest_framework.authtoken',
    'corsheaders',
    'app', # تطبيقك
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware', # يجب أن يكون في الأعلى
    'django.middleware.common.CommonMiddleware',
    # ...
]

# السماح لتطبيق الفلاتر بالاتصال (مهم جداً)
CORS_ALLOW_ALL_ORIGINS = True 

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
}