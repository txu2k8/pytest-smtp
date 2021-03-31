#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : test_1.py
@Time  : 2021/3/31 15:44
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""

import pytest


def test_method1():
    x = 5
    y = 6
    assert x + 1 == y, "test failed"
    assert x == y, "test failed because x=" + str(x) + " y=" + str(y)


def test_method2():
    x = 5
    y = 6
    assert x + 1 == y, "test failed"


if __name__ == '__main__':
    pass
