#!/bin/bash

source ./env

test -f /tmp/ingredientRecipe.db || {
   python3 ../recipe_book/ingredientRecipe/manage.py syncdb
}

python3 ../recipe_book/ingredientRecipe/manage.py runserver --host=0.0.0.0 --port=8003 --debug
