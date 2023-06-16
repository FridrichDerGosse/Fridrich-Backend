"""
fridex/backend/_interface.py

Project: Fridrich-Backend
Created: 13.06.2023
Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

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

    __connection: Connection
    __user: User

    def __init__(self) -> None:
        """
        Create Fridex-Backend
        """
        self.__communication = None

        self.__connection = Connection(self.communication)
        self.__user = User(self.communication)

    def communication(self) -> Communication | None:
        """
        :return: Communication instance if exists
        """
        return self.__communication

    def __set_communication(self, com: Communication | None) -> None:
        """
        Set/Unset communication once connected / disconnected
        :param com: Communication or None
        """
        self.__communication = com

    @property
    def user(self) -> User:
        """
        :return: User SubInterface
        """
        return self.__user
