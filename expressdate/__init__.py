from datetime import date
from .parse import DateParser


def express(expr: str) -> tuple[date, ...]:
    return DateParser.parse(expr)
