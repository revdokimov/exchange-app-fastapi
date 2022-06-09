from sqlalchemy import Column, Integer, String, UniqueConstraint, CheckConstraint

from app.db.base_class import Base

class CurrencyPair(Base):
    id = Column(Integer, primary_key=True, index=True)
    ticker1 = Column(String(3), index = True)
    ticker2 = Column(String(3), index = True)
    __table_args__ = (
        UniqueConstraint(ticker1, ticker2), # unique combination of tickers
        CheckConstraint('length(ticker1) == 3'),
        CheckConstraint('length(ticker2) == 3'),
    )