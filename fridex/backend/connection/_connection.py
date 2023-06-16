"""
fridex/backend/connection/_connection.py

Project: Fridrich-Backend
Created: 14.06.2023
Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from typing import Callable, Any

from ..communication import Communication
from ..default import SubInterface


##################################################
#                     Code                       #
##################################################

class Connection(SubInterface):
    """
    Connection interface
    """
    __set_communication: Callable[[Communication | None], Any]

    def __init__(
            self,
            communication: Callable[[], Communication | None],
            set_communication: Callable[[Communication | None], Any],
    ) -> None:
        """
        Create connection interface
        :param communication: Communication callback
        :param set_communication: Callback to set connection
        """
        super().__init__(communication, "connection")
        self.__set_communication = set_communication

    def login(self, name: str, password: str) -> None:
        """
        Login with username and password
        :param name: Username
        :param password: Password
        """
        self._data_request(("login",), "set", {"name": name, "password": password})

    def logout(self) -> None:
        self._data_request(("logout",), "set", {})

    def connect(self, ip: str, port: int) -> None:
        """
        Connect to server
        :param ip: IP of the server
        :param port: Port to connect
        """
        self.__set_communication(Communication(ip, port))

    def disconnect(self) -> None:
        """
        Disconnect from server
        """
        self._communication.close()
        self.__set_communication(None)
