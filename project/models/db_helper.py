__author__ = 'Or Duan'
from project import db


def save(obj):
    session = db
    session.add(obj)
    session.commit()


def delete(obj):
    session = db
    session.delete(obj)
    session.commit()