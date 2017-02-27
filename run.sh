#!/bin/sh
docker run --name="flaskapi" -d -p 5000:5000 -i tgpc/flaskapi gunicorn --bind 0.0.0.0:5000 --pythonpath /usr/src/ wsgi:app
