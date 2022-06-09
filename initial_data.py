import logging
import csv
import asyncio
from datetime import date
from decimal import Decimal

from app.db.session import SessionLocal
from app.models import CurrencyPair, currency_pair

from sqlalchemy import text

from app.models.exchange_rate import ExchangeRate

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def init() -> None:
    async with SessionLocal() as session:
        with open('app/data/exchange.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            currency_pairs = []
            for currency in reader.fieldnames:
                match currency.split("/"):
                    case [_]:
                        continue
                    case [ticker1, ticker2]:
                        currency_pairs.append(CurrencyPair(ticker1 = ticker1, ticker2 = ticker2))
            
            await session.execute(text("TRUNCATE exchangerate CASCADE"))
            await session.execute(text("TRUNCATE currencypair CASCADE"))
            await session.commit()
            session.add_all(currency_pairs)
            await session.commit()
            for i in currency_pairs:
                await session.refresh(i)
            
            currency_pairs_map = {f"{i.ticker1}/{i.ticker2}":i.id for i in currency_pairs}

            for row in reader:
                d = date.fromisoformat(row["Date"])
                for pair,rate in row.items():
                    if pair == "Date":
                        continue
                    
                    er = ExchangeRate(currencypair_id = currency_pairs_map[pair], rate = Decimal(rate), date = d)
                    session.add(er)
            
            await session.commit()
        
    

def main() -> None:
    logger.info("Creating initial data")
    asyncio.run(init())
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
