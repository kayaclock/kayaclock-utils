"""Utils used across the project"""
from logging import getLogger
from typing import NoReturn

logger = getLogger("kayaclock.assert_never")


def assert_never(value: NoReturn) -> None:
    """This function should never be called

    See https://hakibenita.com/python-mypy-exhaustive-checking
    """
    logger.critical(f"Unhandled value: {value} ({type(value).__name__})")
