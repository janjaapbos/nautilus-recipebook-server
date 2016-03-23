from graphene import Schema, ObjectType, String, Mutation, Boolean, Field, Int
from nautilus.api import ServiceObjectType, Connection
from nautilus.network import dispatch_action
from nautilus.conventions import getCRUDAction
from recipe_book.recipe import service as RecipeService
from recipe_book.ingredient import service as IngredientService
from recipe_book.ingredientRecipe.server import service as IngredientRecipeService


class Recipe(ServiceObjectType):
    class Meta:
        service = RecipeService

    ingredients = Connection('Ingredient')


class Ingredient(ServiceObjectType):
    class Meta:
        service = IngredientService


class IngredientRecipe(ServiceObjectType):
    class Meta:
        service = IngredientRecipeService


class Query(ObjectType):
    ingredients = Connection(Ingredient)
    recipes = Connection(Recipe)
    ingredientrecipes = Connection(IngredientRecipe)


class AddRecipeMutation(Mutation):
    """
        This mutation fires an event to create a new recipe in the model service.
    """
    class Input:
        """
            This class defines the mutation arguments.
        """
        name = String()
        category = String()
        cook_time = Int()


    success = Boolean(description="Whether or not the dispatch was successful")

    @classmethod
    def mutate(cls, instance, args, info):
        """ perform the mutation """
        # send the new recipe action into the queue
        payload = dict(
            name=args['name'],
            category=args['category'],
            cook_time=args['cookTime'],
        )
        dispatch_action(
            action_type=getCRUDAction('create', RecipeService.model),
            payload=payload
        )
        return AddRecipeMutation(success=True)


class AddIngredientMutation(Mutation):
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
        # send the new ingredient action into the queue
        payload = dict(
            name=args['name'],
        )
        dispatch_action(
            action_type=getCRUDAction('create', IngredientService.model),
            payload=payload
        )
        return AddIngredientMutation(success=True)


class AddIngredientRecipeMutation(Mutation):
    """
        This mutation fires an event to connect an ingredient to a recipe in the model service.
    """
    class Input:
        """
            This class defines the mutation arguments.
        """
        ingredient = String()
        recipe = String()


    success = Boolean(description="Whether or not the dispatch was successful")

    @classmethod
    def mutate(cls, instance, args, info):
        """ perform the mutation """
        # send the new ingredientRecipe action into the queue
        payload = dict(
            recipe=args['recipe'],
            ingredient=args['ingredient'],
        )
        dispatch_action(
            action_type=getCRUDAction('create', IngredientRecipeService.model),
            payload=payload
        )
        return AddIngredientRecipeMutation(success=True)


class ApiMutations(ObjectType):
    """ the list of mutations that the api supports """
    addRecipe = Field(AddRecipeMutation)
    addIngredient = Field(AddIngredientMutation)
    addIngredientRecipe = Field(AddIngredientRecipeMutation)


schema = Schema()
schema.query = Query
schema.mutation = ApiMutations
