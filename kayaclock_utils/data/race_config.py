"""Values documenting the configuration of the race"""
from enum import IntEnum
from typing import Sequence

from pydantic import BaseModel

from .basic_types import GateID, RefereePostID


class RefereePost(BaseModel):
    class Config:
        allow_mutation = False

    id: RefereePostID
    gate_ids: Sequence[GateID]


class TimerPosition(IntEnum):
    START = 0
    FINISH = 1
