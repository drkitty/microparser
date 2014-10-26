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
