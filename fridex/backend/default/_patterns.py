"""
fridex/backend/default/_patterns.py

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

from ..communication import PATHS, DATA

from ._subinterface import SubWorker


##################################################
#                     Code                       #
##################################################


class GetSubPattern:
    """
    Default attribute pattern with get and subscribe
    """
    _sub_worker: SubWorker
    _path: PATHS  # Should be set by the child class

    def __init__(
            self,
            sub_worker: SubWorker
    ) -> None:
        """
        Create default attribute pattern
        :param sub_worker: Subscription SubWorker
        """
        self._sub_worker = sub_worker

        self._sub_worker.add_pattern(self._path, self._rework_data)

    def _get(self, **params: DATAUNIT) -> Future[Any]:
        """
        Get value
        :param params: Request parameters
        :return: Future to get result data
        :raise CommunicationNotInitialized: If communication doesn't exist yet.
        """
        return self._sub_worker.data_request(self._path, "get", params)

    def _subscribe(self, callback: Callable[[Any], Any], **params: Any) -> int:
        """
        Subscribe to value
        :param callback: Callback when value is updated
        :param params: Request parameters
        :return: Subscription ID
        :raise CommunicationNotInitialized: If communication doesn't exist yet.
        """
        return self._sub_worker.sub_request(self._path, "sub", params, callback)

    def _rework_data(self, data: DATA) -> Any:
        """
        Rework received data.
        Every subinterface should overwrite this
        :param data: Data to rework
        :return: Reworked data
        """
        ...


class GetSubSetPattern(GetSubPattern):
    """
    Default attribute pattern with get, subscribe and set
    """
    def _set(self, **params: DATAUNIT) -> Future[Any]:
        """
        Set value
        :param params: Set-Request parameters
        :return: Future to get result data
        :raise CommunicationNotInitialized: If communication doesn't exist yet.
        """
        return self._sub_worker.data_request(self._path, "set", params)


class AddDelGetSubPattern(GetSubPattern):
    """
    Default attribute pattern with add, del, get and subscribe
    """
    def _add(self, **params: DATAUNIT) -> Future[Any]:
        """
        Add value
        :param params: Add-Request parameters
        :return: Future to get result data
        :raise CommunicationNotInitialized: If communication doesn't exist yet.
        """
        return self._sub_worker.data_request(self._path, "add", params)

    def _delete(self, **params: DATAUNIT) -> Future[Any]:
        """
        Delete value
        :param params: Delete-Request parameters
        :return: Future to get result data
        :raise CommunicationNotInitialized: If communication doesn't exist yet.
        """
        return self._sub_worker.data_request(self._path, "del", params)
