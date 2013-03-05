#!/usr/bin/python
from setuptools import setup, find_packages


def get_deb_meta():
    with open("debian/changelog") as chlog:
        data = chlog.read()
    return dict(
        name=data[0],
        version=data[1][1:-1]
    )


setup(
    packages = find_packages(exclude=["templates"]),
    entry_points={
        "console_scripts": [
            'marek = marek.main:main'
        ]
    },
    **get_deb_meta()
)
