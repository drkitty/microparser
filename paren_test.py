#!/usr/bin/env python3

from parser import End, char, Invalid, parse, Stream


def group(s):
    if s.get() != '(':
        raise Invalid()
    g = []
    try:
        while True:
            g.append(parse(s, group, char(lambda c: c not in '()'), exc=End))
    except End:
        pass
    if s.get() != ')':
        raise Invalid()
    return g


def main():
    try:
        line = Stream(input())
    except EOFError:
        return
    print(parse(line, group))
    rest = ''.join(line.i)
    if rest:
        print("Warning: Trailing characters: '{}'".format(rest))


if __name__ == '__main__':
    main()
