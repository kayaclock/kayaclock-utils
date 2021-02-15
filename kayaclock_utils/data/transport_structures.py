"""Data structures meant to be stored once and never modified"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from .basic_types import (
    GateID,
    GateResult,
    RunID,
)
from .race_config import TimerPosition
from .validators import validate_datetime_from_iso


class StatusUpdate(BaseModel):
    class Config:
        allow_mutation = False

    run_id: RunID
    creation_timestamp: datetime

    _validate_creation_timestamp: classmethod = validate_datetime_from_iso(
        "creation_timestamp"
    )


class GateStatusUpdate(StatusUpdate):
    gate: GateID
    result: Optional[GateResult]  # if None = remove result for this gate


class TimingUpdate(StatusUpdate):
    timer: TimerPosition
    time: datetime
    _validate_time: classmethod = validate_datetime_from_iso("time")
