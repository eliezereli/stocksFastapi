import datetime

from sqlalchemy import JSON, Boolean, Column, ForeignKey, Numeric, Integer, String,DateTime
from sqlalchemy.orm import relationship

from db import Base

class Stock(Base):
    __tablename__ = "sp500"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(80), unique=True, index=True)
    name = Column(String(80))
    sector = Column(String(80))
    industry = Column(String(80))
    exchange = Column(String(80))
    lastUpdated=Column(DateTime, default=datetime.datetime.utcnow)
    currentPrice = Column(Numeric(10, 2))
    closingPrice=Column(JSON)


