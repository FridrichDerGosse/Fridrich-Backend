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
from hashlib import sha256

from ..communication import Communication
from ..default import SubInterface

from ._patterns import InformationPattern, NamePattern, DoubleVotesPattern, CreationDatePattern


##################################################
#                     Code                       #
##################################################

class User(SubInterface):
    """
    User interface
    """
    __information: InformationPattern
    __name: NamePattern
    __double_votes: DoubleVotesPattern
    __creation_date: CreationDatePattern

    def __init__(self, communication: Callable[[], Communication | None]):
        """
        Create user interface
        :param communication: Communication callback
        """
        super().__init__(communication, "user")

        self.__information = InformationPattern(self._sub_worker)
        self.__name = NamePattern(self._sub_worker)
        self.__double_votes = DoubleVotesPattern(self._sub_worker)
        self.__creation_date = CreationDatePattern(self._sub_worker)

    @staticmethod
    def __hash(value: str) -> str:
        """
        Password hashing
        :param value: To hash
        :return: Hashed
        """
        return sha256(value.encode("UTF-8")).hexdigest()

    def register(self, name: str, password: str) -> None:
        """
        Register new user (set)
        :param name: Username
        :param password: Password of the user
        """
        self._sub_worker.data_request(
            "register", "set",
            {"name": name, "password": self.__hash(password)}
        )

    def change_password(self, old_password: str, new_password: str) -> None:
        """
        Change password (set)
        :param old_password: Old password to confirm access
        :param new_password: New password
        """
        self._sub_worker.data_request(
            "password", "set",
            {"old": self.__hash(old_password), "new": self.__hash(new_password)})

    @property
    def information(self) -> InformationPattern:
        """
        :return: Information attribute
        """
        return self.__information

    @property
    def name(self) -> NamePattern:
        """
        :return: Name attribute
        """
        return self.__name

    @property
    def double_votes(self) -> DoubleVotesPattern:
        """
        :return: DoubleVote attribute
        """
        return self.__double_votes

    @property
    def creation_date(self) -> CreationDatePattern:
        """
        :return: CreationDate attribute
        """
        return self.__creation_date
