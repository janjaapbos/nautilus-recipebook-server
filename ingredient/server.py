# third party imports
from nautilus import ModelService
# third party imports
from sqlalchemy import Column, Text
from nautilus.models import HasID, BaseModel, CRUDNotificationCreator

class Ingredient(CRUDNotificationCreator, HasID, BaseModel):
    name = Column(Text)


class ServiceConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/ingredient.db'


service = ModelService(
    configObject = ServiceConfig,
    model = Ingredient,
)
