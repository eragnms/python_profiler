# -*- coding: utf-8 -*-
import io
import os
import re

from setuptools import setup


def read(*names, **kwargs):
    with io.open(
        os.path.join(os.path.dirname(__file__), *names),
        encoding=kwargs.get("encoding", "utf8"),
    ) as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


with open("README.rst") as f:
    readme = f.read()

with open("LICENSE") as f:
    license = f.read()

setup(
    name="simpleprofiler",
    version=find_version("simpleprofiler/simpleprofiler.py"),
    description="A template for my python projects",
    long_description=readme,
    author="Mats Gustafsson",
    author_email="matsgus71@gmail.com",
    url="https://github.com/eragnms/simpleprofiler",
    license=license,
    entry_points={
        "console_scripts": ["simpleprofiler = simpleprofiler.simpleprofiler:main"]
    },
    packages=["simpleprofiler"],
    install_requires=[
        "package_1",
        "package_2",
    ],
)
