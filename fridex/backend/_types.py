"""
fridex/backend/_types.py

Project: Fridrich-Backend
Created: 14.06.2023
Author: Lukas Krahbichler
"""

##################################################
#                    Imports                     #
##################################################

from typing import TypedDict, Literal, Any


##################################################
#                     Code                       #
##################################################

SECTIONS = Literal["connection", "user", "voting"]

CONNECTION_PATHS = tuple[Literal["a"], Literal["b"]]
USER_PATHS = tuple[Literal["c"], Literal["b"]]
VOTING_PATHS = tuple[Literal["a"], Literal["b"]]


class DataRequest(TypedDict):
    section: SECTIONS
    path: CONNECTION_PATHS | USER_PATHS | VOTING_PATHS


class DataResponse(TypedDict):
    section: SECTIONS
    data: Any
