from __future__ import annotations

from setuptools import find_packages
from setuptools import setup

VERSION = "0.0.1"
DESCRIPTION = "Pricegram Search Engine"
LONG_DESCRIPTION = (
    "Search Engine Implementation of Pricegram, "
    "an ecommerce product comparison website."
)

# Setting up
setup(
    name="pricegram_search",
    version=VERSION,
    author="geetu040",
    author_email="raoarmaghanshakir040@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=["python", "first package", "search engine"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
)
