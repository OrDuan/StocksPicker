from sqlalchemy import Column, ForeignKey, DateTime, Float, Integer, String
from project import Base

__author__ = 'Or Duan'


class History(Base):
    __tablename__ = 'history'

    id = Column(Integer, primary_key=True)
    symbol = Column(String(10), ForeignKey("stock.symbol"))
    date = Column(DateTime)
    high = Column(Float)
    low = Column(Float)
    open = Column(Float)
    close = Column(Float)
    volume = Column(Integer)

    def __init__(self, symbol, date, high, low, open, close, volume):
        self.symbol = symbol
        self.date = date
        self.high = high
        self.low = low
        self.open = open
        self.close = close
        self.volume = volume

    def __repr__(self):
        return "< History: " + self.symbol + " Date: " + str(self.date) + " >"