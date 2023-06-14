"""
fridex/backend/communication/communication.py

Project: Fridrich-Backend
Created: 14.06.2023
Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from fridex.connection import ClientConnection, DATAUNIT


##################################################
#                     Code                       #
##################################################

class Communication(ClientConnection):
    """
    Communication to server
    """

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

    def __request_data(self, _req: DATAUNIT) -> DATAUNIT:  # noqa
        """
        Yet, not data can be requested from the client
        :param _req: Data request
        :return: Requested data
        """
        return {}

    def __rework_data(self, data: DATAUNIT) -> DATAUNIT:  # noqa - TEMP
        """
        Rework received data, before passing it to futures or subscriptions
        :param data: Data to rework
        :return: Reworked data
        """
        return data

