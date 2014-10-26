#!/usr/bin/env python3

from unittest import TestLoader


if __name__ == '__main__':
    TestLoader().discover('tests').debug()
