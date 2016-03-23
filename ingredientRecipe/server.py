# third party imports
from nautilus import ConnectionService

# import the services to connect
from recipe_book.ingredient import service as ingredient_service
from recipe_book.recipe import service as recipe_service

class ServiceConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/ingredientRecipe.db'

service = ConnectionService(
    configObject=ServiceConfig,
    services=[
        ingredient_service,
        recipe_service,
    ]
)
