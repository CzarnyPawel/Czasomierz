# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'czasomierz',
        'HOST': '127.0.0.1',
        'PASSWORD': 'coderslab',
        'USER': 'postgres',
        'PORT': 5432
    }
}