from graphene import Schema, ObjectType, String, Mutation, Boolean, Field
from nautilus.api import ServiceObjectType, Connection
from nautilus.network import dispatch_action
from nautilus.conventions import getCRUDAction
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


class AddRecipeMutation(Mutation):
    """
        This mutation fires an event to create a new recipe in the model service.
    """
    class Input:
        """
            This class defines the mutation arguments.
        """
        name = String()


    success = Boolean(description="Whether or not the dispatch was successful")

    @classmethod
    def mutate(cls, instance, args, info):
        """ perform the mutation """
        # send the new recipe action into the queue
        payload = dict(name=args['name'])
        dispatch_action(
            action_type=getCRUDAction('create', RecipeService.model),
            payload=payload
        )


class ApiMutations(ObjectType):
    """ the list of mutations that the api supports """
    addRecipe = Field(AddRecipeMutation)


schema = Schema()
schema.query = Query
schema.mutation = ApiMutations
