import imp
from app.db.session import database
from fastapi import Query, HTTPException
from fastapi_crudrouter import DatabasesCRUDRouter
from app.schemas.exchange_rate import ExchangeRate, ExchangeRateCreate, HistoryRate, RateWithPath
from app import models
from app.db.base import Base
from sqlalchemy import select

from decimal import Decimal, getcontext
import datetime
from itertools import chain, combinations, permutations

getcontext().prec = 4

table = Base.metadata.tables[models.ExchangeRate.__tablename__]
DATE_REGEXP = "^\d{4}-\d{2}-\d{2}$" # incomplete date regexp

router = DatabasesCRUDRouter(
    schema=ExchangeRate,
    create_schema=ExchangeRateCreate,
    table=table,
    database=database
)

@router.get("/history/", response_model=list[HistoryRate])
async def history(
    currencypair : str = Query(default=..., min_length=7, max_length=7, regex="^[A-Z]{3}/[A-Z]{3}$"),
    start_date : str = Query(default=None, min_length=10, max_length=10, regex=DATE_REGEXP),
    end_date : str = Query(default=None, min_length=10, max_length=10, regex=DATE_REGEXP)
):
    "Get history data for currency pair"
    ticker1, ticker2 = currencypair.split("/")
    query = select(models.ExchangeRate).join(models.ExchangeRate.currencypair).where(
        models.CurrencyPair.ticker1 == ticker1,
        models.CurrencyPair.ticker2 == ticker2
        )
    if start_date:
        query = query.where(models.ExchangeRate.date >= datetime.date.fromisoformat(start_date))

    if end_date:
        query = query.where(models.ExchangeRate.date <= datetime.date.fromisoformat(end_date))

    rates = await database.fetch_all(query)

    return [HistoryRate(date = i.date, rate = i.rate) for i in rates]


@router.get("/rate/", response_model=RateWithPath)
async def rate(
    currencypair : str = Query(default=..., min_length=7, max_length=7, regex="^[A-Z]{3}/[A-Z]{3}$"),
    date : str = Query(default=..., min_length=10, max_length=10, regex=DATE_REGEXP)
):
    "Get rate for particular date and currency pair"
    ticker1, ticker2 = currencypair.split("/")
    if ticker1 == ticker2:
        # conversion rate to itself is always 1.0000
        return HistoryRate(date = datetime.date.fromisoformat(date), rate = Decimal("1.0000"))

    query = select(models.ExchangeRate).where(
        models.ExchangeRate.date == datetime.date.fromisoformat(date)
        )

    # get all rates for that day
    rates = await database.fetch_all(query)
    
    tickers = set() # set for unique tickers, they are graph nodes
    edges = {}

    for i in rates:
        tickers.add(i.ticker1)
        tickers.add(i.ticker2)
        edges[(i.ticker1, i.ticker2)] = i.rate # add direct conversion
        edges[(i.ticker2, i.ticker1)] = Decimal(1) / i.rate # add reverse conversion with reverse rate

    if (ticker1, ticker2) in edges:
        # if direct conversion possible return it immediately
        return RateWithPath(date = datetime.date.fromisoformat(date), rate = edges[(ticker1, ticker2)], path = [ticker1, ticker2])
    
    min_rate = Decimal('Inf')
    min_path = None
    
    tickers.difference_update({ticker1, ticker2})
    tickers = list(tickers)

    for r in range(len(tickers)+1):
        for path in permutations(tickers, r):
            rate = Decimal(1)
            path = list(path)
            path.insert(0, ticker1)
            path.append(ticker2)

            for t1, t2 in zip(path, path[1:]):
                if (t1,t2) not in edges:
                    break
                rate *= edges[(t1,t2)]
            else:
                if rate < min_rate:
                    min_rate = rate
                    min_path = path

    if not min_path:
        raise HTTPException(status_code=400, detail="Conversion not found")
    else:
        return RateWithPath(date = datetime.date.fromisoformat(date), rate = min_rate, path = min_path)
