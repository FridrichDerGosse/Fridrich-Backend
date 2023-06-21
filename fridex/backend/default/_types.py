"""
fridex/backend/default/_types.py

Project: Fridrich-Backend
Created: 14.06.2023
Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from typing import TypedDict, Literal, Union


##################################################
#                     Code                       #
##################################################

SECTIONS = Literal["connection", "user", "voting"]
REQ_TYPES = Literal["get", "sub", "set", "add", "del"]

CONNECTION_PATHS = Literal["login", "logout"]
USER_PATHS = Literal["register", "password", "name", "double_votes", "permission_level", "information"]
VOTING_PATHS = Literal["information"]
PATHS = Union[CONNECTION_PATHS, USER_PATHS, VOTING_PATHS]


class DataRequest(TypedDict):
    section: SECTIONS
    type: REQ_TYPES
    path: PATHS
    params: dict[str | int | float | bool | None, any]


class DataResponse(TypedDict):
    path: PATHS
    data: dict[str | int | float | bool | None, any]
