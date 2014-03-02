# Testing 

TESTING=True
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = 'log/app-emails' # change this to a proper location
AUTHENTICATOR  = open("/home/abhiram/.tor/control_auth_cookie","r").read().strip()



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': "WeatherDB",                      # Or path to database file if using sqlite3.
        'TEST_NAME': 'WeatherTestDB',
        'USER': '',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}
