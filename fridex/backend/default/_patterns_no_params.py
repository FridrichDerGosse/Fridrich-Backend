"""
fridex/backend/default/_patterns_no_params.py

Project: Fridrich-Backend
Created: 25.06.2023
Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from concurrent.futures import Future
from typing import Any, Callable

from ._patterns_super import GetSubPattern, GetSubSetPattern, AddDelGetSubPattern


##################################################
#                     Code                       #
##################################################

class NoParamsGetSubPattern(GetSubPattern):
    """
    GetSubPattern that takes no params
    """
    def get(self) -> Future[Any]:
        """
        Get value
        :return: Future to get result data
        :raise CommunicationNotInitialized: If communication doesn't exist yet.
        """
        return self._get()

    def subscribe(self, callback: Callable[[Any], Any]) -> int:
        """
        Subscribe to value
        :param callback: Callback when value is updated
        :return: Subscription ID
        :raise CommunicationNotInitialized: If communication doesn't exist yet.
        """
        return self._subscribe(callback)


class NoParamsGetSubSetPattern(NoParamsGetSubPattern, GetSubSetPattern):
    """
    GetSubSetPattern that takes no params
    """
    def set(self) -> Future[Any]:
        """
        Set value
        :return: Future to get result data
        :raise CommunicationNotInitialized: If communication doesn't exist yet.
        """
        return self._set()


class NoParamsAddDelGetSubPattern(NoParamsGetSubPattern, AddDelGetSubPattern):
    """
    AddDelGetSubPattern that takes no params
    """
    def add(self) -> Future[Any]:
        """
        Add value
        :return: Future to get result data
        :raise CommunicationNotInitialized: If communication doesn't exist yet.
        """
        return self._add()

    def delete(self) -> Future[Any]:
        """
        Delete value
        :return: Future to get result data
        :raise CommunicationNotInitialized: If communication doesn't exist yet.
        """
        return self._delete()
