from datetime import datetime
from typing import Union

from pydantic import validator


def _datetime_from_iso(dt: Union[str, datetime]) -> datetime:
    if isinstance(dt, str):
        dt = datetime.fromisoformat(dt)
    assert dt.tzinfo is not None
    return dt


def validate_datetime_from_iso(*fields: str) -> classmethod:
    return validator(*fields, allow_reuse=True, pre=True)(_datetime_from_iso)
