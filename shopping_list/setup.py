# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 15:07:48 2020

@author: kbootsri
"""

from setuptools import find_packages, setup

setup(
    name='shopping_list',
    version='1.0.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask',
    ],
)