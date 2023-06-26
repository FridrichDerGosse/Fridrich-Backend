"""
fridex/backend/communication/communication.py

Project: Fridrich-Backend
Created: 14.06.2023
Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from fridex.connection import ClientConnection, ProtocolInterface, DATAUNIT
from typing import Any, Callable, Tuple

from ._types import DataResponse, SECTIONS, PATHS, DATA


##################################################
#                     Code                       #
##################################################

class Communication(ClientConnection):
    """
    Communication to server
    """
    __patterns: dict[Tuple[SECTIONS, PATHS], Callable[[DATA], Any]]

    def __init__(
            self,
            ip: str,
            port: int
    ) -> None:
        """
        Create connection to server
        :param ip: IP of the server
        :param port: Port to connect
        """
        super().__init__(ip=ip, port=port,
                         request_callback=self.__request_data,
                         rework_callback=self.__rework_data)
        self.__patterns = {}

    def __request_data(self, _req: DATAUNIT) -> DATAUNIT:  # noqa
        """
        Yet, not data can be requested from the client
        :param _req: Data request
        :return: Requested data
        """
        return {}

    def __rework_data(self, data: DataResponse) -> Any:
        """
        Rework received data, before passing it to futures or subscriptions
        :param data: Data to rework
        :return: Reworked data
        """
        return self.__patterns[data["section"], data["path"]](data["data"])

    def add_pattern(self, section: SECTIONS, path: PATHS, rework: Callable[[DATA], Any]) -> None:
        """
        Add a rework callback for a pattern
        :param section: Section of the subinterface
        :param path: Path of the pattern
        :param rework: Callback to rework received response data
        """
        self.__patterns[section, path] = rework

    @property
    def protocol(self) -> ProtocolInterface:
        """
        :return: Protocol instance
        """
        return self._protocol

