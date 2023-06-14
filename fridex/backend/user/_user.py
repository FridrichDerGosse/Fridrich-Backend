"""
fridex/backend/user/_user.py

Project: Fridrich-Backend
Created: 14.06.2023
Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from concurrent.futures import Future
from ..communication import Communication


##################################################
#                     Code                       #
##################################################

class User:
    """
    User interface
    """
    def __init__(self, communication_future: Future[Communication]):
        ...

    def register(self, name: str, password: str) -> None:
        """
        Register new user
        :param name: Username
        :param password: password of the user
        """
