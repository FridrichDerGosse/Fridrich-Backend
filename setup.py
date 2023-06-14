"""
/setup.py

Project: Fridrich-Connection
Created: 23.05.2023
Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from setuptools import find_packages, setup
from pathlib import Path


##################################################
#                     Code                       #
##################################################

here = Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="fridex-backend",
    version="0.0.0",
    description="Fridrich bakcend",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Lukas Krahbichler",
    author_email="melonenbuby@proton.me",
    url="https://github.com/FridrichDerGosse/Fridrich-Backend",
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    keyword="dashboard, voting, connection, bakcend",
    packages=find_packages(),
    namespace_packages=['fridex'],
    python_requires=">=3.11"
)
