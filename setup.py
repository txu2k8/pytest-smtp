#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@file  : setup.py
@Time  : 2021/2/7 9:57
@Author: Tao.Xu
@Email : tao.xu2008@outlook.com
"""

import os
import codecs
from setuptools import setup, find_packages


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding='utf-8').read()


setup(
    name='pytest-smtp',
    version='1.0.2',
    author='Tao Xu',
    author_email='txu2008@outlook.com',
    maintainer='Tao Xu',
    maintainer_email='txu2008@outlook.com',
    license='BSD-3',
    keywords=['pytest', 'py.test', 'smtp', 'email'],
    url='https://github.com/txu2k8/pytest-smtp',
    description='A plugin for send email with pytest execution result once execution is completed.',
    long_description=read('README.rst'),
    py_modules=['pytest_smtp'],
    packages=find_packages(include=['pytest_smtp']),
    setup_requires=['pytest-runner', ],
    python_requires='>=3.5',
    install_requires=[
        'pytest>=6.2.2',
        'pytest-runner'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Framework :: Pytest',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Testing',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: BSD License',
    ],
    entry_points={
        'pytest11': [
            'smtp = pytest_smtp',
            'pytest-smtp = pytest_smtp.plugin',
        ],
    },
)


if __name__ == '__main__':
    pass
