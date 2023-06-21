"""
fridex/backend/default/_subinterface.py

Project: Fridrich-Backend
Created: 14.06.2023
Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from fridex.connection import DATAUNIT
from concurrent.futures import Future
from typing import Callable, Any

from ._types import SECTIONS, PATHS, DataRequest, REQ_TYPES, DataResponse
from ..communication import Communication


##################################################
#                     Code                       #
##################################################

class CommunicationNotInitialized(Exception):
    ...


class SubInterface:
    """
    Default SubInterface
    """
    _communication_callback: Callable[[], Communication | None]
    _communication: Communication | None
    _section: SECTIONS

    __subscription_id: int | None
    __subscription_callbacks: dict[PATHS, list[Callable[[Any], Any]]]

    def __init__(self, communication: Callable[[], Communication | None], type_: SECTIONS) -> None:
        """
        Create Interface
        :param communication: Communication callback
        :param type_: SubInterface Type
        """
        self._communication_callback = communication
        self._communication = None
        self._section = type_

        self.__subscription_id = None
        self.__subscription_callbacks = {}

    def __build_req_dict(self, path: PATHS, type_: REQ_TYPES, params: DATAUNIT) -> DataRequest:
        """
        Build request dictonary
        :param path: Request path
        :param type_: Request type
        :param params: Request parameters
        :return: Request dictonary
        """
        return {
            "section": self._section,
            "type": type_,
            "path": path,
            "params": params
        }

    def _data_request(self, path: PATHS, type_: REQ_TYPES, params: DATAUNIT) -> Future[Any]:
        """
        Add data request
        :param path: Request path
        :param type_: Request type
        :param params: Request parameters
        :return: Future to get result data
        :raise CommunicationNotInitialized: If communication doesn't exist yet.
        """
        if not self._communication:
            self._communication = self._communication_callback()
        if self._communication:
            return self._communication.protocol.data.request_add(self.__build_req_dict(path, type_, params))

        raise CommunicationNotInitialized("Communication doesn't exist yet.")

    def _sub_request(self, path: PATHS, type_: REQ_TYPES, params: DATAUNIT, callback: Callable[[Any], Any]) -> int:
        """
        Send add subscription
        :param path: Request path
        :param type_: Request type
        :param params: Request parameters
        :param callback: Callback when value is updated
        :return: Subscription ID
        """
        if not self._communication:
            self._communication = self._communication_callback()
        if self._communication:
            if not self.__subscription_id:
                self.__subscription_id = self._communication.add_subscription(
                    self.__work_subscription,
                    self.__build_req_dict("information", type_, params)
                )

            if not self.__subscription_callbacks[path]:
                self.__subscription_callbacks[path] = []
            self.__subscription_callbacks[path].append(callback)

    def __work_subscription(self, value: DataResponse) -> None:
        """
        Work on the end callbacks
        :param value: Whole value packet
        """
        for arg in value["data"]:
            if arg in self.__subscription_callbacks:
                for callback in self.__subscription_callbacks[arg]:
                    callback(value["data"][value["path"]])

        if "information" in self.__subscription_callbacks:
            for callback in self.__subscription_callbacks["information"]:
                callback(value["data"])

    def unsubscribe(self, path: PATHS, callback: Callable[[Any], Any]) -> None:
        """
        Remove certain subscription
        :param path: Request path
        :param callback: Callback when value is updated
        """
        self.__subscription_callbacks[path].remove(callback)
        if not self.__subscription_callbacks[path]:
            self.__subscription_callbacks.pop(path)

        if len(self.__subscription_callbacks) == 0:
            self._communication.delete_subscription(self.__subscription_id)
            self.__subscription_id = None
