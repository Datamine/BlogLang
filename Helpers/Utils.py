"""
Miscellaneous utilities that don't fit
anywhere else in the helpers
"""

def joinit(iterable, delimiter):
    """
    intersperse a list with copies of an element
    from http://stackoverflow.com/a/5656097
    """
    it = iter(iterable)
    yield next(it)
    for x in it:
        yield delimiter
        yield x
