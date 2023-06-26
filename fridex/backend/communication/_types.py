"""
fridex/backend/communication/_types.py

Project: Fridrich-Backend
Created: 14.06.2023
Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from typing import TypedDict, Literal, Union, Dict


##################################################
#                     Code                       #
##################################################

SECTIONS = Literal["connection", "user", "voting"]
REQ_TYPES = Literal["get", "sub", "set", "add", "del"]

CONNECTION_PATHS = Literal["login", "logout"]
USER_PATHS = Literal["register", "password", "name", "double_votes", "permission_level", "information", "creation_date"]
VOTING_PATHS = Literal["information"]
PATHS = Union[CONNECTION_PATHS, USER_PATHS, VOTING_PATHS]
DATA = Dict[str | int | float | bool | None, any]


class DataRequest(TypedDict):
    section: SECTIONS
    type: REQ_TYPES
    path: PATHS
    params: DATA


class DataResponse(TypedDict):
    section: SECTIONS
    path: PATHS
    data: DATA
