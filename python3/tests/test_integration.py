"""I *think* these are integration tests."""

from unittest import TestCase

from parser import End, char, Invalid, Stream


def group(s):
    if s.get() != '(':
        raise Invalid()
    g = []
    try:
        while True:
            g.append(s.parse(group, char(lambda c: c not in '()'), exc=End))
    except End:
        pass
    if s.get() != ')':
        raise Invalid()
    return g


class ParenTests(TestCase):
    def test_valid1(self):
        s = Stream('()')
        self.assertEqual(s.parse(group), [])

    def test_valid2(self):
        s = Stream('(())')
        self.assertEqual(s.parse(group), [[]])

    def test_valid3(self):
        s = Stream('(012(3456)7)')
        self.assertEqual(
            s.parse(group), ['0', '1', '2', ['3', '4', '5', '6'], '7'])
