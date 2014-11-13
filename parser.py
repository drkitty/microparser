from contextlib import contextmanager
from itertools import tee
from traceback import print_stack


class Invalid(Exception):
    pass


class End(Exception):
    pass


class Stream(object):
    def __init__(self, iterable=None):
        self.b = []  # backtrackable chars
        self.u = []  # ungot chars
        if iterable is None:
            self.i = None
        else:
            self.i = iter(iterable)

    def get(self):
        if self.u:
            c = self.u.pop(0)
        else:
            c = next(self.i, None)
        if c is not None:
            self.b.append(c)
        #print_stack(limit=2)
        print("... get {}".format(repr(c)))
        return c

    def __enter__(self):
        dup = Stream()
        dup.i = self.i
        dup.u = self.u
        self.child = dup
        return dup

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_type in (End, Invalid):
            print("... unget '{}'".format(''.join(self.child.b)))
            self.u.extend(self.child.b)


def parse(s, *fs, exc=Invalid):
    for f in fs:
        try:
            with s as ss:
                return f(ss)
        except Invalid:
            pass
    raise exc()


def char(cond):
    def inner(s):
        c = s.get()
        if c is None or not cond(c):
            raise Invalid()
        return c
    return inner
