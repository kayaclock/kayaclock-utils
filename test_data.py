import functools
from datetime import datetime, timezone
from typing import Callable, Set, NewType, Any, Tuple

import pytest
from pydantic import ValidationError

from kayaclock_utils.config import gate_count
from kayaclock_utils.data.basic_types import RunID, GateResult
from kayaclock_utils.data.db_models import Racer
from kayaclock_utils.data.enums import (
    Penalisation,
    MissReason,
)
from kayaclock_utils.data.transport_structures import GateStatusUpdate

WrappedF = NewType("WrappedF", Callable[..., Any])


def assert_pydantic_validation_errors(
        excs: Set[Tuple[Tuple[str, ...], str]]
) -> Callable[[WrappedF], WrappedF]:
    def decorator(f: WrappedF) -> WrappedF:
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            v = None
            with pytest.raises(ValidationError) as err_info:
                v = f(*args, **kwargs)
            assert set((e["loc"], e["type"]) for e in err_info.value.errors()) == excs
            return v

        return wrapper

    return decorator


# noinspection PyMethodMayBeStatic
class TestRunID:
    def test_assigned_valid(self):
        r = RunID(assigned_number=1)
        r = RunID(assigned_number=2)

    @assert_pydantic_validation_errors(
        {(("assigned_number",), "value_error.const"), (("__root__",), "assertion_error")})
    def test_assigned_invalid(self):
        r = RunID(assigned_number=0)

    def test_extra_valid(self):
        r = RunID(other_id="uniqfoobar")


class TestGateResult:
    def test_valid_miss(self):
        r = GateResult.parse_obj({"penalisation": 50, "miss_reason": "A"})
        assert r.penalisation is Penalisation.MISS and r.miss_reason is MissReason.A

    def test_valid_touch(self):
        r = GateResult.parse_obj({"penalisation": 2})
        assert r.penalisation is Penalisation.TOUCH and r.miss_reason is None

    def test_valid_good(self):
        r = GateResult.parse_obj({"penalisation": 0})
        assert r.penalisation is Penalisation.GOOD and r.miss_reason is None

    @assert_pydantic_validation_errors({(("miss_reason",), "assertion_error")})
    def test_missing_miss_reason(self):
        r = GateResult.parse_obj({"penalisation": 50})

    @assert_pydantic_validation_errors({(("miss_reason",), "assertion_error")})
    def test_miss_reason_on_touch(self):
        r = GateResult.parse_obj({"penalisation": 2, "miss_reason": "A"})

    @assert_pydantic_validation_errors({(("penalisation",), "value_error.missing")})
    def test_required_penalisation(self):
        r = GateResult.parse_obj({})


class TestDBRacer:
    def test_final_time_full(self):
        r = Racer.parse_obj(
            {
                "id": 1,
                "reg_numbers": ["foo"],
                "perf_class": "M",
                "gender_category": "M",
                "boat_category": "K1",
                "age_category": "DM",
                "runs": [
                    {
                        "start_time": "2000-01-01T00:00:00.000000+00:00",
                        "finish_time": "2000-01-01T00:01:42.168496+00:00",
                        "penalisations": [{"penalisation": 50, "miss_reason": "C"}, {"penalisation": 2}] + [None] * (
                                gate_count - 2),
                    },
                    {
                        "start_time": "2000-01-01T00:00:00.000000+00:00",
                        "finish_time": "2010-01-01T00:00:00.000000+00:00",
                    },
                ],
            }
        )
        assert r.final_time == 60 + 42.168496 + 2 + 50

    def test_one_run(self):
        r = Racer.parse_obj(
            {
                "id": 1,
                "reg_numbers": ["foo"],
                "perf_class": "M",
                "gender_category": "M",
                "boat_category": "K1",
                "age_category": "DM",
                "runs": [
                    {
                        "start_time": "2000-01-01T00:00:00.000000+00:00",
                        "finish_time": "2000-01-01T01:00:00.000000+00:00",
                    },
                    {},
                ],
            }
        )
        assert r.final_time == 3600

    @pytest.mark.parametrize(
        "boat_category,reg_numbers_count",
        [("C1", 0), ("C1", 2), ("C1", 3), ("K1", 2), ("C2", 0), ("C2", 1), ("C2", 3)],
    )
    @assert_pydantic_validation_errors({(("reg_numbers",), "value_error.tuple.length")})
    def test_invalid_reg_numbers_count(self, boat_category, reg_numbers_count):
        r = Racer.parse_obj(
            {
                "id": 1,
                "perf_class": "M",
                "gender_category": "M",
                "age_category": "DM",
                "boat_category": boat_category,
                "reg_numbers": ["foo"] * reg_numbers_count,
            }
        )


class TestGateStatusUpdate:
    def test_timestamp_date(self):
        u = GateStatusUpdate(run_id=RunID(assigned_number=1),
                             creation_timestamp=datetime(1970, 1, 1, tzinfo=timezone.utc), gate=1)

    def test_timestamp_iso(self):
        u = GateStatusUpdate(run_id=RunID(assigned_number=2), creation_timestamp="1970-01-01T00:00:00+00:00", gate=1)

    @assert_pydantic_validation_errors({(("creation_timestamp",), "assertion_error")})
    def test_timestamp_iso_without_tz(self):
        u = GateStatusUpdate(run_id=RunID(assigned_number=2), creation_timestamp="1970-01-01T00:00:00", gate=1)
