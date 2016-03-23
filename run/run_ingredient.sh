#!/bin/bash

source ./env

test -f /tmp/ingredient.db || {
   python3 ../recipe_book/ingredient/manage.py syncdb
}

python3 ../recipe_book/ingredient/manage.py runserver --host=0.0.0.0 --port=8002 --debug
