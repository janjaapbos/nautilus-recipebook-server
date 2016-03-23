#!/bin/bash

source ./env

test -f /tmp/recipe.db || {
   python3 ../recipe_book/recipe/manage.py syncdb
}

python3 ../recipe_book/recipe/manage.py runserver --host=0.0.0.0 --port=8001 --debug
