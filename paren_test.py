#!/usr/bin/env python3

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
        rest = ''.join(line.i)
        if rest:
            print("Warning: Trailing characters: '{}'".format(rest))


if __name__ == '__main__':
    main()
