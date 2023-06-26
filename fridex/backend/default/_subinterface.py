"""
fridex/backend/default/_subinterface.py

Project: Fridrich-Backend
Created: 14.06.2023
Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from typing import Callable, Any, Tuple
from fridex.connection import DATAUNIT
from concurrent.futures import Future

from ..communication import Communication, SECTIONS, PATHS, DataRequest, REQ_TYPES, DataResponse, DATA


##################################################
#                     Code                       #
##################################################

class CommunicationNotInitialized(Exception):
    ...


class SubWorker:
    """
    Basically the background part of the SubInterface
    """
    __communication_callback: Callable[[], Communication | None]
    __communication: Communication | None
    __section: SECTIONS

    __subscription_callbacks: dict[PATHS, list[Callable[[Any], Any]]]
    __subscription_id: int | None

    __add_patterns: list[Tuple[PATHS, Callable[[DATA], Any]]]

    def __init__(
            self,
            communication: Callable[[], Communication | None],
            section: SECTIONS,
    ) -> None:
        """
        Create Interface Worker
        :param communication: Communication callback
        :param section: SubInterface Section
        """
        self.__communication_callback = communication
        self.__communication = None
        self.__section = section

        self.__subscription_callbacks = {}
        self.__subscription_id = None

        self.__add_patterns = []

    def add_pattern(self, path: PATHS, rework: Callable[[DATA], Any]) -> None:
        """
        Add a rework callback for a pattern
        :param path: Path of the pattern
        :param rework: Callback to rework received response data
        """
        if self.__communication:
            self.__communication.add_pattern(self.__section, path, rework)
        else:
            self.__add_patterns.append((path, rework))

    def check_communication(self) -> None:
        """
        Check if communication exists
        """
        if not self.__communication:
            self.__communication = self.__communication_callback()
            for add in self.__add_patterns:
                self.__communication.add_pattern(self.__section, *add)

        if not self.__communication:
            raise CommunicationNotInitialized("Communication doesn't exist yet.")

    def __build_req_dict(self, path: PATHS, type_: REQ_TYPES, params: DATAUNIT) -> DataRequest:
        """
        Build request dictonary
        :param path: Request path
        :param type_: Request type
        :param params: Request parameters
        :return: Request dictonary
        """
        return {
            "section": self.__section,
            "type": type_,
            "path": path,
            "params": params
        }

    def data_request(self, path: PATHS, type_: REQ_TYPES, params: DATAUNIT) -> Future[Any]:
        """
        Add data request
        :param path: Request path
        :param type_: Request type
        :param params: Request parameters
        :return: Future to get result data
        :raise CommunicationNotInitialized: If communication doesn't exist yet.
        """
        self.check_communication()
        return self.__communication.protocol.data.request_add(self.__build_req_dict(path, type_, params))

    def sub_request(self, path: PATHS, type_: REQ_TYPES, params: DATAUNIT, callback: Callable[[Any], Any]) -> int:
        """
        Send add subscription
        :param path: Request path
        :param type_: Request type
        :param params: Request parameters
        :param callback: Callback when value is updated
        :return: Subscription ID
        :raise CommunicationNotInitialized: If communication doesn't exist yet.
        """
        self.check_communication()

        if not self.__subscription_id:
            self.__subscription_id = self.__communication.add_subscription(
                self.__work_subscription,
                self.__build_req_dict("information", type_, params)
            )

        if not self.__subscription_callbacks[path]:
            self.__subscription_callbacks[path] = []
        self.__subscription_callbacks[path].append(callback)
        return self.__subscription_id

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

    @property
    def communication(self) -> Communication | None:
        """
        :return: Communication if exists
        """
        return self.__communication

    @property
    def subscription_callbacks(self) -> dict[PATHS, list[Callable[[Any], Any]]]:
        """
        :return: Subscription callbacks dict
        """
        return self.__subscription_callbacks

    @property
    def subscription_id(self) -> int | None:
        """
        :return: Subscription ID
        """
        return self.__subscription_id

    @subscription_id.setter
    def subscription_id(self, id_: int) -> None:
        """
        :param id_: Set new subscription_id
        """
        self.__subscription_id = id_


class SubInterface:
    """
    Default SubInterface
    """
    _sub_worker: SubWorker

    def __init__(
            self,
            communication: Callable[[], Communication | None],
            section: SECTIONS
    ) -> None:
        """
        Create Interface
        :param communication: Communication callback
        :param section: SubInterface Section
        """
        self._sub_worker = SubWorker(communication, section)

    def unsubscribe(self, path: PATHS, callback: Callable[[Any], Any]) -> None:
        """
        Remove certain subscription
        :param path: Request path
        :param callback: Callback when value is updated
        :raise CommunicationNotInitialized: If communication doesn't exist yet.
        """
        self._sub_worker.check_communication()

        self._sub_worker.subscription_callbacks[path].remove(callback)
        if not self._sub_worker.subscription_callbacks[path]:
            self._sub_worker.subscription_callbacks.pop(path)

        if len(self._sub_worker.subscription_callbacks) == 0:
            self._sub_worker.communication.delete_subscription(self._sub_worker.subscription_id)
            self._sub_worker.subscription_id = None
