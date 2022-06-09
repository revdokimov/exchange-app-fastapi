from locale import currency
from pydantic import BaseModel
from .currency_pair import CurrencyPair
from datetime import date
from decimal import Decimal

class ExchangeRateCreate(BaseModel):
    currencypair_id: int
    date: date
    rate: Decimal

class ExchangeRate(ExchangeRateCreate):
    id: int
    # currencypair: CurrencyPair

    class Config:
        orm_mode = True

class HistoryRate(BaseModel):
    date: date
    rate: Decimal

class RateWithPath(HistoryRate):
    path: list[str]