#!/bin/bash

echo "collect static files"
python manage.py collectstatic --noinput

echo "apply database migrations"
python manage.py migrate

echo "start uwsgi server"
uwsgi --ini uwsgi.ini