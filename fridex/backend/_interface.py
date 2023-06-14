"""
fridex/backend/_interface.py

Project: Fridrich-Backend
Created: 13.06.2023
Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from concurrent.futures import Future

from .communication import Communication
from .connection import Connection
from .user import User


##################################################
#                     Code                       #
##################################################

class Backend:
    """
    Fridex-Backend
    """
    __communication: Communication | None
    __communication_future: Future[Communication]

    __connection: Connection
    __user: User

    def __init__(self) -> None:
        """
        Create Fridex-Backend
        """
        self.__communication_future = Future()
        self.__communication = None

        self.__connection = Connection()
        self.__user = User()
