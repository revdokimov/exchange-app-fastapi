from pydantic import BaseModel

class CurrencyPairCreate(BaseModel):
    ticker1: str
    ticker2: str

class CurrencyPair(CurrencyPairCreate):
    id: int

    class Config:
        orm_mode = True

