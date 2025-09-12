cd app
gunicorn --bind 0.0.0.0:5000 --timeout 120 --workers 2 wsgi:app
