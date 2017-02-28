#!/bin/sh

running=$(docker inspect --format="{{ .State.Running }}" flaskapi 2>/dev/null || true)
if [ "$running" != "" ]; then
    if [ "$running" == "true" ]; then
        docker stop flaskapi
    fi
    docker rm flaskapi
fi

docker run --name="flaskapi" -d -p 5000:5000 -i tgpc/flaskapi gunicorn --bind 0.0.0.0:5000 --pythonpath /usr/src/ wsgi:app
