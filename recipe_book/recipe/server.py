# third party imports
from nautilus import ModelService
# third party imports
from sqlalchemy import Column, Text, Integer
from nautilus.models import HasID, BaseModel, CRUDNotificationCreator

class Recipe(CRUDNotificationCreator, HasID, BaseModel):
    name = Column(Text)
    category = Column(Text)
    cook_time = Column(Integer)

class ServiceConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/recipe.db'


service = ModelService(
    configObject = ServiceConfig,
    model = Recipe,
)
