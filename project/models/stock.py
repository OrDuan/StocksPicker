from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from project import Base

__author__ = 'Or Duan'


class Stock(Base):
    __tablename__ = 'stock'

    id = Column(Integer)
    symbol = Column(String(10), primary_key=True)
    name = Column(String(150))
    category = Column(String(100))
    location = Column(String(300))

    history = relationship("History", backref="stock.symbol")

    def __init__(self, symbol, name, category, location):
        self.symbol = symbol
        self.name = name
        self.category = category
        self.location = location

    def __repr__(self):
        return "< Stock: " + self.symbol + " >"