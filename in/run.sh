#!/bin/sh

running=$(docker inspect --format="{{ .State.Running }}" flaskapiin 2>/dev/null || true)
if [ "$running" != "" ]; then
    if [ "$running" == "true" ]; then
        docker stop flaskapiin
    fi
    docker rm flaskapiin
fi

docker run --name="flaskapiin" -d -p 5000:5000 -v $PWD/src/uploads:/usr/src/app/uploads -i tgpc/flaskapiin gunicorn --bind 0.0.0.0:5000 --pythonpath /usr/src/ wsgi:app
