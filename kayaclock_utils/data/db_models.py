from __future__ import annotations

from datetime import datetime
from typing import Dict, Optional, Tuple, List, Any

from pydantic import BaseModel, validator, TupleLengthError, Field, conlist

from .basic_types import GateResult, RacerID, RegNumbers
from .enums import AgeCategory, BoatCategory, GenderCategory, PerformanceRating
from .validators import validate_datetime_from_iso
from ..config import gate_count


class Person(BaseModel):
    reg_no: str  # CZ are numbers, but foreign can contain letters
    first_name: str
    surname: str
    male: bool
    birth_year: int
    club: str


class RacerRun(BaseModel):
    start_time: Optional[datetime]
    finish_time: Optional[datetime]
    penalisations: conlist(
        Optional[GateResult], min_items=gate_count, max_items=gate_count
    ) = Field(default_factory=lambda: [None] * gate_count)
    comment: Optional[str]

    _validate_times: classmethod = validate_datetime_from_iso(
        "start_time", "finish_time"
    )

    @property
    def clean_time(self) -> Optional[float]:
        if self.start_time is None or self.finish_time is None:
            return None
        return (self.finish_time - self.start_time).total_seconds()

    @property
    def total_penalisations(self) -> int:
        t = 0
        for penalisation in self.penalisations:
            if penalisation is not None:
                t += penalisation.penalisation.value
        return t

    @property
    def full_time(self) -> Optional[float]:
        ct = self.clean_time
        if ct is None:
            return None
        return ct + self.total_penalisations


class Racer(BaseModel):
    id: RacerID
    perf_class: PerformanceRating
    gender_category: GenderCategory
    boat_category: BoatCategory
    age_category: AgeCategory
    reg_numbers: RegNumbers
    runs: Tuple[RacerRun, RacerRun] = Field(
        default_factory=lambda: (RacerRun(), RacerRun())
    )
    other_runs: Dict[str, RacerRun] = Field(default_factory=dict)

    @validator("reg_numbers")
    def _validate_reg_numbers_count(
        cls, reg_numbers: List[str], values: Dict[str, Any]
    ) -> List[str]:
        if "boat_category" in values:
            l = len(reg_numbers)
            boat_c = values["boat_category"]
            expected_l = 2 if boat_c is BoatCategory.C2 else 1
            if l != expected_l:
                raise TupleLengthError(actual_length=l, expected_length=expected_l)
        return reg_numbers

    @property
    def final_time(self) -> Optional[float]:
        res = None
        for run in self.runs:
            t = run.full_time
            if t is not None and (res is None or t < res):
                res = t
        return res
