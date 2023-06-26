"""
fridex/backend/user/_patterns.py

Project: Fridrich-Backend
Created: 26.06.2023
Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from typing import Callable, Any, TypedDict, NotRequired, Literal
from concurrent.futures import Future
from datetime import datetime

from ..default import GetSubSetPattern, GetSubPattern


##################################################
#                     Code                       #
##################################################

class RawUserInformation(TypedDict):
    name: NotRequired[str]
    double_votes: NotRequired[int]
    creation_date: NotRequired[float]


class UserInformation(TypedDict):
    name: NotRequired[str]
    double_votes: NotRequired[int]
    creation_date: NotRequired[datetime]


class UserReworker:
    @staticmethod
    def rework_date(data: RawUserInformation) -> UserInformation:
        """
        Rework received userdata
        :param data: User information
        :return: Processed user information
        """
        processed: UserInformation = {}

        key: Literal["name", "double_votes", "creation_date"]
        for key, value in data.items():
            match key:
                case "creation_date":
                    processed[key] = datetime.fromtimestamp(value)
                case _:
                    processed[key] = value
        return processed


class InformationPattern(GetSubPattern):
    """
    All information of the user
    """
    _path = "information"
    _type = UserInformation

    def get(self) -> Future[UserInformation]:
        """
        Get all information of the user
        :return: Future that will contain all information
        """
        return self._get()

    def subscribe(self, callback: Callable[[_type], Any]) -> int:
        """
        Subscribe to all information of the user
        :param callback: Callback when a value is updated
        :return: ID of the subscription
        """
        return self._subscribe(callback)

    def _rework_data(self, data: RawUserInformation) -> _type:
        return UserReworker.rework_date(data)


class NamePattern(GetSubSetPattern):
    """
    Name of the user
    """
    _path = "name"
    _type = str

    def get(self) -> Future[_type]:
        """
        Get the name of the user
        :return: Future that will contain the name of the user
        """
        return self._get()

    def subscribe(self, callback: Callable[[_type], Any]) -> int:
        """
        Subscribe to the name of the user
        :param callback: Callback when value is updated
        :return: ID of the subscription
        """
        return self._subscribe(callback)

    def set(self, name: _type) -> Future[bool]:
        """
        Set a new name
        :param name: New username
        :return: Future that tells whether the set was successful
        """
        return self._set(name=name)

    def _rework_data(self, data: RawUserInformation) -> _type:
        return UserReworker.rework_date(data)["name"]


class DoubleVotesPattern(GetSubSetPattern):
    """
    DoubleVotes of the user
    """
    _path = "double_votes"
    _type = int

    def get(self) -> Future[_type]:
        """
        Get the doublevote amount of the user
        :return: Future that will tell the amount of doublevotes
        """
        return self._get()

    def subscribe(self, callback: Callable[[_type], Any]) -> int:
        """
        Subscribe to the doublevote amount of the user
        :param callback: Callback when value is updated
        :return: ID of the subscription
        """
        return self._subscribe(callback)

    def _rework_data(self, data: RawUserInformation) -> _type:
        return UserReworker.rework_date(data)["double_votes"]


class CreationDatePattern(GetSubPattern):
    """
    CreationDate of the user
    """
    _path = "creation_date"
    _type = datetime

    def get(self) -> Future[_type]:
        """
        Get the date when the user was created
        :return: Future that will tell the date
        """
        return self._get()

    def subscribe(self, callback: Callable[[_type], Any]) -> int:
        """
        Subscribe to the date when the user was created.

        (This is quite unnecessary)
        :param callback: Callback when value is updated
        :return: ID of the subscription
        """
        return self._subscribe(callback)

    def _rework_data(self, data: RawUserInformation) -> datetime:
        return UserReworker.rework_date(data)["creation_date"]
