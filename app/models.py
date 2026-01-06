from pydantic import BaseModel
from datetime import datetime


class MarketData(BaseModel):
    ticker: str
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int
