# -*- coding: utf-8 -*-
__author__ = 'Or Duan'
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
engine = create_engine('mysql://root:@localhost/StocksPicker')

Session = sessionmaker(bind=engine)
db = Session()

Base = declarative_base()


# Models
import models.history
import models.stock

