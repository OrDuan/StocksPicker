__author__ = 'or'
from collections import namedtuple


def make_tuple(kwargs):
    returned_obj = namedtuple('returned_obj', kwargs)
    for key, value in kwargs.iteritems():
        setattr(returned_obj, key, value)
    return returned_obj