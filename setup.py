import re
import ast
from setuptools import setup, find_packages

setup(
    name="kblom",
    author="Kim Blomqvist",
    author_email="kblomqvist@iki.fi",
    description="Kim Blomqvist's personal Python library",
    license="MIT",
    version="dev",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "numpy",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.4",
        "License :: OSI Approved :: MIT License",
    ],
    url="https://github.com/kblomqvist/kblom.py",
    download_url="https://github.com/kblomqvist/kblom.py/tarball/master",
)
