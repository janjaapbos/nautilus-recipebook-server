# third party imports
from nautilus import ConnectionService

# import the services to connect
from recipeBook.ingredient import service as ingredient_service
from recipeBook.recipe import service as recipe_service

class ServiceConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/ingredientRecipe.db'

service = ConnectionService(
    configObject=ServiceConfig,
    services=[
        ingredient_service,
        recipe_service,
    ]
)
