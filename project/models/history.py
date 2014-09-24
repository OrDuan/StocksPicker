from sqlalchemy.ext.hybrid import hybrid_property
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
    sma_5_days = Column(Float)
    sma_10_days = Column(Float)
    sma_20_days = Column(Float)
    sma_50_days = Column(Float)
    sma_100_days = Column(Float)
    p_sma_5_days = Column(Float)
    p_sma_10_days = Column(Float)
    p_sma_20_days = Column(Float)
    p_sma_50_days = Column(Float)
    p_sma_100_days = Column(Float)
    mean_deviation_5 = Column(Float)
    mean_deviation_10 = Column(Float)
    mean_deviation_20 = Column(Float)
    mean_deviation_50 = Column(Float)
    mean_deviation_100 = Column(Float)

    def __init__(self, **kwargs):
        self.symbol = kwargs.get('symbol')
        self.date = kwargs.get('date')
        self.high = kwargs.get('high')
        self.low = kwargs.get('low')
        self.open = kwargs.get('open')
        self.close = kwargs.get('close')
        self.volume = kwargs.get('volume')
        self.sma_5_days =kwargs.get('sma_5_days', None)
        self.sma_10_days = kwargs.get('sma_10_days', None)
        self.sma_20_days = kwargs.get('sma_20_days', None)
        self.sma_50_days = kwargs.get('sma_50_days', None)
        self.sma_100_days = kwargs.get('sma_100_days', None)
        self.p_sma_5_days = kwargs.get('p_sma_5_days', None)
        self.p_sma_10_days = kwargs.get('p_sma_10_days', None)
        self.p_sma_20_days = kwargs.get('p_sma_20_days', None)
        self.p_sma_50_days = kwargs.get('p_sma_50_days', None)
        self.p_sma_100_days = kwargs.get('p_sma_100_days', None)
        self.mean_deviation_50 = kwargs.get('mean_deviation_50', None)
        self.mean_deviation_20 = kwargs.get('mean_deviation_20', None)
        self.mean_deviation_100 = kwargs.get('mean_deviation_100', None)
        self.mean_deviation_5 = kwargs.get('mean_deviation_5', None)
        self.mean_deviation_10 = kwargs.get('mean_deviation_10', None)

    def __repr__(self):
        return "< History: " + self.symbol + " Date: " + str(self.date) + " >"

    @hybrid_property
    def p(self):
        return (self.high + self.low + self.close) / 3