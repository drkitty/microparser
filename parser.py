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
        self.q = []  # queue
        if iterable is None:
            self.i = iter(())
        else:
            self.i = iter(iterable)

    def next(self):
        return next(self.i, None)

    def get(self):
        if self.q:
            c = self.q.pop(0)
        else:
            c = self.next()
        if c is not None:
            self.b.append(c)
        return c

    def parse(self, *fs, exc=Invalid):
        for f in fs:
            try:
                with self as ss:
                    return f(ss)
            except Invalid:
                pass
        raise exc()

    def __enter__(self):
        dup = self.__class__()
        dup.i = self.i
        dup.q = self.q
        self.child = dup
        return dup

    def __exit__(self, exc_type, exc_value, traceback):
        self.q = self.child.q
        if exc_type in (End, Invalid):
            self.child.b.extend(self.q)
            self.q = self.child.b


class FileStream(Stream):
    def __init__(self, filename=None):
        if filename is None:
            f = None
        else:
            f = open(filename, 'r')
        super().__init__(f)


    def fetch_line(self):
        line = next(self.i, None)
        if line is None:
            return
        for c in line:
            self.q.append(c)

    def next(self):
        self.fetch_line()
        return self.q.pop(0)



def char(cond):
    def inner(s):
        c = s.get()
        if c is None or not cond(c):
            raise Invalid()
        return c
    return inner
