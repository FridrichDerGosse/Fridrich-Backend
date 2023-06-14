"""
fridex/backend/default/_attribut_patterns.py

Project: Fridrich-Backend
Created: 14.06.2023
Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from fridex.connection import MessageDict, DATAUNIT
from concurrent.futures import Future
from typing import Callable, Any

from ._types import PATHS, REQ_TYPES


##################################################
#                     Code                       #
##################################################

DATA_REQUEST_TYPE = Callable[[PATHS, REQ_TYPES, DATAUNIT], Future[MessageDict]]
ADD_SUB_TYPE = Callable[[PATHS, REQ_TYPES, DATAUNIT, Callable[[Any], Any]], int]


class GetSubPattern:
    """
    Default attribute pattern with get and subscribe
    """
    _data_request_callback: DATA_REQUEST_TYPE
    _add_sub_callback: ADD_SUB_TYPE
    _path: PATHS

    def __init__(
            self,
            data_request_callback: DATA_REQUEST_TYPE,
            add_subscription_callback: ADD_SUB_TYPE,
            path: PATHS
    ) -> None:
        """
        Create default attribute pattern
        :param data_request_callback: Data request callback
        :param add_subscription_callback: Send add subscription request callback
        :param path: Path of this attribute
        """
        self._data_request_callback = data_request_callback
        self._add_sub_callback = add_subscription_callback
        self._path = path

    def get(self, params: DATAUNIT) -> Future[Any]:
        """
        Get value
        :param params: Request parameters
        :return: Future to get result data
        :raise CommunicationNotInitialized: If communication doesn't exist yet.
        """
        return self._data_request_callback(self._path, "get", params)

    def subscribe(self, params: DATAUNIT, callback: Callable[[Any], Any]) -> int:
        """
        Subscribe to value
        :param params: Request parameters
        :param callback: Callback when value is updated
        :return: Subscription ID
        :raise CommunicationNotInitialized: If communication doesn't exist yet.
        """
        return self._add_sub_callback(self._path, "sub", params, callback)


class GetSubSetPattern(GetSubPattern):
    """
    Default attribute pattern with get, subscribe and set
    """
    def get(self, params: DATAUNIT) -> Future[Any]:
        """
        Set value
        :param params: Set-Request parameters
        :return: Future to get result data
        :raise CommunicationNotInitialized: If communication doesn't exist yet.
        """
        return self._data_request_callback(self._path, "get", params)


class AddDelGetSubPattern(GetSubPattern):
    """
    Default attribute pattern with add, del, get and subscribe
    """
    def add(self, params: DATAUNIT) -> Future[Any]:
        """
        Add value
        :param params: Add-Request parameters
        :return: Future to get result data
        :raise CommunicationNotInitialized: If communication doesn't exist yet.
        """
        return self._data_request_callback(self._path, "add", params)

    def delete(self, params: DATAUNIT) -> Future[Any]:
        """
        Delete value
        :param params: Delete-Request parameters
        :return: Future to get result data
        :raise CommunicationNotInitialized: If communication doesn't exist yet.
        """
        return self._data_request_callback(self._path, "del", params)

