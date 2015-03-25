#!/usr/bin/env python3

from unittest import TestLoader


if __name__ == '__main__':
    runner = TestLoader().discover('tests')
    print('Running {} tests...'.format(runner.countTestCases()))
    runner.debug()
    print('All tests passed.')
