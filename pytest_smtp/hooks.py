#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : hooks.py
@Time  : 2021/3/31 15:32
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""


def pytest_smtp_report_title(report):
    """ Called before adding the title to the report """


def pytest_smtp_results_summary(prefix, summary, postfix):
    """ Called before adding the summary section to the report """


def pytest_smtp_results_table_header(cells):
    """ Called after building results table header. """


def pytest_smtp_results_table_row(report, cells):
    """ Called after building results table row. """


def pytest_smtp_results_table_html(report, data):
    """ Called after building results table additional HTML. """

