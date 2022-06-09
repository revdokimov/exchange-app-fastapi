from app.db.session import database
from fastapi_crudrouter import DatabasesCRUDRouter
from app.schemas.currency_pair import CurrencyPair, CurrencyPairCreate
from app import models
from app.db.base import Base

router = DatabasesCRUDRouter(
    schema=CurrencyPair,
    create_schema=CurrencyPairCreate,
    table=Base.metadata.tables[models.CurrencyPair.__tablename__],
    database=database
)