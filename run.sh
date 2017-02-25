#!/bin/sh
docker run --name="flaskapi" --network="host" -d -p 5000:5000 -e "FLASK_APP=/usr/src/app/flaskapi.py" -i tgpc/flaskapi flask run
