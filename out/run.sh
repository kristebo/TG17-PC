#!/bin/sh

running=$(docker inspect --format="{{ .State.Running }}" flaskapiout 2>/dev/null || true)
if [ "$running" != "" ]; then
    if [ "$running" == "true" ]; then
        docker stop flaskapiout
    fi
    docker rm flaskapiout
fi

docker run --name="flaskapiout" -d -p 5000:5000 -i tgpc/flaskapiout gunicorn --bind 0.0.0.0:5000 --pythonpath /usr/src/ wsgi:app
