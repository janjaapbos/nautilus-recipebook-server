#! /usr/bin/env python3

from nautilus import ServiceManager

# local imports
from recipeBook.ingredientRecipe.server import service

# create a manager wrapping the service
manager = ServiceManager(service)

if __name__ == '__main__':
    manager.run()
