"""Definitions of purpose-specific type aliases

See typing.NewType
"""
from __future__ import annotations

from typing import Dict, NewType, Optional, Tuple, Any, Union, Literal

from pydantic import (
    PositiveInt,
    validator,
    BaseModel,
    root_validator,
)

from .enums import MissReason, Penalisation

RacerID = NewType("RacerID", PositiveInt)

RefereePostID = NewType("RefereePostID", PositiveInt)

GateID = NewType("GateID", PositiveInt)

RegistrationNumber = NewType("RegistrationNumber", str)

RegNumbers = Union[
    Tuple[RegistrationNumber], Tuple[RegistrationNumber, RegistrationNumber]
]


class RunID(BaseModel):
    """Identifier of a single run of a single racer

    Is one of the following:
    - {assigned_number: 1}
    - {assigned_number: 2}
    - {other_id: <str>}
    """

    class Config:
        allow_mutation = False

    assigned_number: Optional[Literal[1, 2]]
    other_id: Optional[str]

    @root_validator
    def _validate_run_id_fields(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        assert (values.get("assigned_number") is None) != (
            values.get("other_id") is None
        ), "Exactly one of assigned_number, other_id must be specified"
        return values


class GateResult(BaseModel):
    class Config:
        allow_mutation = False

    penalisation: Penalisation
    miss_reason: Optional[MissReason]

    @validator("miss_reason", always=True)
    def _validate_miss_reason_presence(
        cls, v: Optional[MissReason], values: Dict[str, Any]
    ) -> Optional[MissReason]:
        if "penalisation" in values:
            assert (v is not None) == (
                values["penalisation"] is Penalisation.MISS
            ), "miss reason must be set when, and only when, the gate was missed"
        return v
