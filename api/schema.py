from graphene import String, ObjectType, Schema
from nautilus.api import ServiceObjectType, Connection
from recipeBook.recipe import service as RecipeService
from recipeBook.ingredient import service as IngredientService


class Recipe(ServiceObjectType):
    class Meta:
        service = RecipeService

    ingredients = Connection('Ingredient')


class Ingredient(ServiceObjectType):
    class Meta:
        service = IngredientService


class Query(ObjectType):
    ingredients = Connection(Ingredient)
    recipes = Connection(Recipe)


schema = Schema()
schema.query = Query
