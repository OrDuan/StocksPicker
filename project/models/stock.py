from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from project import Base

__author__ = 'Or Duan'


class Stock(Base):
    __tablename__ = 'stock'

    id = Column(Integer)
    symbol = Column(String(10), primary_key=True)
    history = relationship("History", backref="stock.symbol")

    def __init__(self, symbol):
        self.symbol = symbol


    def __repr__(self):
        return "< Stock: " + self.symbol + " >"