#!/usr/bin/env python3

import json
import click
import requests
import random
import string
import sys
import time


def random_string():
    return(''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6)))

def dump_json(var):
    s = json.dumps(
        var,
        indent=2,
        sort_keys=True
    )
    return(s)

def do_graphql(url, query):
    r = requests.post(
                      url,
                      data=query,
                      headers = {'Content-type': 'application/graphql'}
    )
    print(r.status_code)
    print(r.text)
    return(json.loads(r.text))

def get_recipe(url, recipe):
    query = """query {
  recipes (name: "%(name)s", category: "%(type)s") {
    edges {
      node {
        id
        name
        category
        primaryKey
        ingredients {
          edges {
            node {
              id
              name
              primaryKey
            }
          }
        }
      }
    }
  }
}""" % recipe
    print(query)
    return(do_graphql(url, query))

def create_recipe(url, recipe):
    mutation = """mutation {
  addRecipe (name: "%(name)s", category: "%(type)s", cookTime: %(cook_time)s) {
    success
  }
}""" % recipe

    print(mutation)
    return(do_graphql(url, mutation))

def get_ingredient(url, ingredient_name):
    query = """query {
  ingredients (name: "%(ingredient_name)s") {
    edges {
      node {
        id
        name
        primaryKey
      }
    }
  }
}""" % locals()
    print(query)
    return(do_graphql(url, query))

def create_ingredient(url, ingredient_name):
    mutation = """mutation {
  addIngredient (name: "%(ingredient_name)s") {
    success
  }
}""" % locals()

    print(mutation)
    return(do_graphql(url, mutation))

def create_ingredient_recipe(url, ingredient_key, recipe_key):
    mutation = """mutation {
  addIngredientRecipe (ingredient: "%(ingredient_key)s", recipe: "%(recipe_key)s") {
    success
  }
}""" % locals()

    print(mutation)
    return(do_graphql(url, mutation))


@click.command()
@click.option('--count', default=1, help='Number of iterations.')
@click.option('--random/--no-random', default=False, help='Add random string to name')
@click.option('--fname', default='recipes.json', prompt='JSON file to load',
              help='The JSON file that contains the entries to load')
@click.option('--url', default='http://localhost:8000/graphql',
              prompt='URL of the Nautilus API service',
              help='The API service tp connect to')
def load_data(count, fname, url, random):
    recipes = json.loads(open(fname).read())
    while count > 0:
        ingredients_dict = {}
        for recipe in recipes:
            for ingredient_name in recipe['ingredients']:
                result = get_ingredient(url, ingredient_name)
                data = result.get("data")
                errors = result.get("errors")
                if errors:
                    print("<<<ERROR>>>")
                    print(dump_json(errors))
                    sys.exit()
                if not data['ingredients']['edges']:
                    create_ingredient(url, ingredient_name)
                    result = get_ingredient(url, ingredient_name)
                    data = result.get("data")
                    errors = result.get("errors")
                    if errors:
                        print("<<<ERROR>>>")
                        print(dump_json(errors))
                        sys.exit()
                    time.sleep(0.1)
                    result = get_ingredient(url, ingredient_name)
                    data = result.get("data")
                ingredient_key =  data['ingredients']['edges'][0]['node']['primaryKey']
                ingredient_id =  data['ingredients']['edges'][0]['node']['id']
                name =  data['ingredients']['edges'][0]['node']['name']
                assert ingredient_name == name, "Igredient name is not the same!"
                ingredients_dict[ingredient_name] = dict(
                     key=ingredient_key,
                     id=ingredient_id
                )

        for recipe in recipes:
            recipe = recipe.copy()
            if random:
                recipe['name'] = random_string() + " " + recipe['name']
            result = get_recipe(url, recipe)
            data = result.get("data")
            errors = result.get("errors")
            if errors:
                print("<<<ERROR>>>")
                print(dump_json(errors))
                sys.exit()
            if not data['recipes']['edges']:
                result = create_recipe(url, recipe)
                data = result.get("data")
                errors = result.get("errors")
                if errors:
                    print("<<<ERROR Creating recipe>>>")
                    print(dump_json(errors))
                    sys.exit()
                elif not data['addRecipe']['success']:
                    print("<<<ERROR No success creating recipe>>>")
                    sys.exit()
                time.sleep(0.1)
                result = get_recipe(url, recipe)
                data = result.get("data")
            print("data:", data)
            recipe_key = data['recipes']['edges'][0]['node']['primaryKey']
            ingredients = data['recipes']['edges'][0]['node']['ingredients']['edges']
            need_to_create = recipe['ingredients'][:]
            for ingredient in ingredients:
                print("ingredient", ingredient)
                if ingredient['node']['name'] in need_to_create:
                    need_to_create.remove(ingredient['node']['name'])
            for name in need_to_create:
                ingredient_key = ingredients_dict[name]['key']
                create_ingredient_recipe(url, ingredient_key, recipe_key)
           
        count -= 1


if __name__ == "__main__":
    load_data()
