"""Main module."""


def fn1():
    '''First function'''
    pass


def fn2():
    '''Second function'''
    pass

def add(x,y):
    """Add Function
    
    :param x: x
    :type x: int, float
    :param y: y
    :type y: int, float
    """
    return x + y

def subtract(x, y):
    """Subtract Function
    
    :param x: x
    :type x: int, float
    :param y: y
    :type y: int, float
    """
    return  x - y

def multiply(x, y):
    """Multiply Function"""
    return x * y

def divide(x, y):
    """Divide Function"""
    if y ==:
        raise ValueError('Can not divide by zero!')
    return x / y
