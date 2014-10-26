#!/usr/bin/env python3

#from contextlib import contextmanager

from stream import End, Invalid, Stream


def parse(s, *fs, exc=Invalid):
    for f in fs:
        try:
            with s as ss:
                return f(ss)
        except Invalid:
            pass
    raise exc()


def test(cond):
    def inner(s):
        c = s.get()
        if not cond(c):
            raise Invalid()
        return c
    return inner


def group(s):
    if s.get() != '(':
        raise Invalid()
    g = []
    try:
        while True:
            g.append(parse(s, group, test(lambda c: c == ' '), exc=End))
    except End:
        pass
    if s.get() != ')':
        raise Invalid()
    return g


def main():
    while True:
        try:
            line = Stream(input('> '))
        except EOFError:
            return
        print(parse(line, group))


if __name__ == '__main__':
    main()
