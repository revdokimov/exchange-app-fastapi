from sqlalchemy import Column, Integer, Date, Numeric, UniqueConstraint, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class ExchangeRate(Base):
    id = Column(Integer, primary_key=True, index=True)
    currencypair_id = Column(Integer, ForeignKey("currencypair.id"))
    currencypair = relationship("CurrencyPair", lazy='joined')
    date = Column(Date, index=True)
    rate = Column(Numeric(scale = 4), index=True)
    __table_args__ = (
        UniqueConstraint(date, currencypair_id), # unique rate for given pair per day
    )