# Konfigurasi server Gunicorn
bind = '0.0.0.0:8000'
workers = 4

# Pengaturan aplikasi Flask
FLASK_APP = 'app:app'
FLASK_ENV = 'production'

# Pengaturan log
LOG_FILENAME = 'app.log'
