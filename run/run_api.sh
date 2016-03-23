#!/bin/bash

source ./env || {
  echo "Please copy env.template to env"
  exit
}

python3 ../recipe_book/api/manage.py runserver --host=0.0.0.0 --port=8000 --debug
