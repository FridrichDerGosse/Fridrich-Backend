"""
fridex/backend/default/_types.py

Project: Fridrich-Backend
Created: 14.06.2023
Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from typing import TypedDict, Literal, Any, Tuple, Union


##################################################
#                     Code                       #
##################################################

SECTIONS = Literal["connection", "user", "voting"]
REQ_TYPES = Literal["get", "sub", "set", "add", "del"]

CONNECTION_PATHS = Tuple[Literal[""]]
USER_PATHS = Tuple[Literal["register", "password", "name", "double_votes", "permission_level"]]
VOTING_PATHS = Tuple[Literal[""]]
PATHS = Union[CONNECTION_PATHS, USER_PATHS, VOTING_PATHS]


class DataRequest(TypedDict):
    section: SECTIONS
    type: REQ_TYPES
    path: PATHS
    params: dict


class DataResponse(TypedDict):
    section: SECTIONS
    data: Any
