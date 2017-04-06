#!/bin/sh

running=$(docker inspect --format="{{ .State.Running }}" flaskapiout 2>/dev/null || true)
if [ "$running" != "" ]; then
    if [ "$running" == "true" ]; then
        docker stop flaskapiout
    fi
    docker rm flaskapiout
fi

docker run --name="flaskapiout" -d -p 4900:4900 -v $PWD/src/uploads:/usr/src/app/uploads -i tgpc/flaskapiout gunicorn --bind 0.0.0.0:4900 --pythonpath /usr/src/ wsgi:app
