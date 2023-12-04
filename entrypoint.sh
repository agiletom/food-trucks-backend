#!/bin/bash

# Wait for the database to be ready
while ! nc -z db 5432; do   
  sleep 0.1
done

# Apply database migrations
python manage.py migrate

# Load initial data into the database
python manage.py loaddata backend/fixtures/initial_data.json

# Start Gunicorn
exec gunicorn --bind 0.0.0.0:8000 backend.wsgi:application
