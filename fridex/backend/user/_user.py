"""
fridex/backend/user/_user.py

Project: Fridrich-Backend
Created: 14.06.2023
Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from typing import Callable

from ..default import SubInterface, GetSubSetPattern, GetSubPattern
from ..communication import Communication


##################################################
#                     Code                       #
##################################################

class User(SubInterface):
    """
    User interface
    """
    __name: GetSubSetPattern
    __double_votes: GetSubPattern
    __permission_level: GetSubPattern

    def __init__(self, communication: Callable[[], Communication | None]):
        """
        Create user interface
        :param communication: Communication callback
        """
        super().__init__(communication, "user")

        self.__name = GetSubSetPattern(self._data_request, self._sub_request, ("name",))
        self.__double_votes = GetSubPattern(self._data_request, self._sub_request, ("double_votes",))
        self.__permission_level = GetSubPattern(self._data_request, self._sub_request, ("permission_level",))

    def register(self, name: str, password: str) -> None:
        """
        Register new user (set)
        :param name: Username
        :param password: password of the user
        """
        self._data_request(("register",), "set", {"name": name, "password": password})

    def password(self, old_password: str, new_password: str) -> None:
        """
        Change password (set)
        :param old_password: Old password to confirm access
        :param new_password: New password
        """
        self._data_request(("password",), "set", {"old": old_password, "new": new_password})

    @property
    def name(self) -> GetSubSetPattern:
        """
        :return: Name attribute
        """
        return self.__name

    @property
    def double_votes(self) -> GetSubPattern:
        """
        :return: DoubleVote attribute
        """
        return self.__double_votes

    @property
    def permission_level(self) -> GetSubPattern:
        """
        :return: PermissionLevel attribute
        """
        return self.__permission_level
