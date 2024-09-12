#!/bin/bash

echo -n "Database migrations, if any... "
poetry run python ./src/manage.py migrate
echo "done."

echo "Starting uvicorn..."
poetry run python ./src/manage.py runserver 0.0.0.0:8000
