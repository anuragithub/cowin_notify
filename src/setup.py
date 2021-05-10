import os


from pip._internal.req import parse_requirements
from setuptools import find_packages, setup

VERSION = "0.1.1"
setup(
    name="cowin_search",
    version=VERSION,
    description="",
    long_description_content_type="text/markdown",
    packages=find_packages(include=["cowin_search"]),
    install_reqs=parse_requirements("../requirements.txt", session="hack"),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)