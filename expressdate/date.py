from __future__ import annotations
from datetime import date, timedelta
from .parse import DateParser


class Date:
    def __init__(self, expr: date | str):
        if isinstance(expr, str):
            self._expr = expr
            self._date = DateParser.parse(expr)
        elif isinstance(expr, date):
            self._expr = expr.strftime("%m-%d-%Y")
            self._date = (expr,)
        else:
            raise TypeError("Invalid type.")

    def __hash__(self) -> int:
        return hash(self._date)

    def __str__(self) -> str:
        return self._expr

    def __repr__(self) -> str:
        return f"Date('{self._expr}')"

    def __add__(self, other: timedelta | int) -> tuple[date, ...]:
        if isinstance(other, int):
            other = timedelta(days=other)
        return tuple(i + other for i in self._date)

    def __radd__(self, other: timedelta) -> tuple[date, ...]:
        return self.__add__(other)

    def __sub__(self, other: Date | tuple[date, ...]) -> tuple[date, ...]:
        if isinstance(other, Date):
            return tuple(sorted(set(self._date) - set(other.dates)))
        elif isinstance(other, tuple):
            return tuple(sorted(set(self._date) - set(other)))
        raise TypeError("Invalid type.")

    def __rsub__(self, other: Date | tuple[date, ...]) -> tuple[date, ...]:
        if isinstance(other, Date):
            return tuple(sorted(set(other.dates) - set(self._date)))
        elif isinstance(other, tuple):
            return tuple(sorted(set(other) - set(self._date)))
        raise TypeError("Invalid type.")

    def __xor__(self, other: Date | tuple[date, ...]) -> tuple[date, ...]:
        if isinstance(other, Date):
            return tuple(sorted(set(self._date) ^ set(other._date)))
        elif isinstance(other, tuple):
            return tuple(sorted(set(self._date) ^ set(other)))
        raise TypeError("Invalid type.")

    def __rxor__(self, other: Date | tuple[date, ...]) -> tuple[date, ...]:
        if isinstance(other, Date):
            return tuple(sorted(set(other.dates) ^ set(self._date)))
        elif isinstance(other, tuple):
            return tuple(sorted(set(other) ^ set(self._date)))
        raise TypeError("Invalid type.")

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Date):
            return hash(self) == hash(other)
        elif isinstance(other, date):
            return self._date == (other,)
        elif isinstance(other, str):
            return hash(self) == hash(Date(other))
        return False

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __or__(self, other: Date | tuple[date, ...]) -> tuple[date, ...]:
        if isinstance(other, Date):
            return tuple(sorted(set(self._date) | set(other._date)))
        elif isinstance(other, tuple):
            return tuple(sorted(set(self._date) | set(other)))
        raise TypeError("Invalid type.")

    def __ror__(self, other: Date | tuple[date, ...]) -> tuple[date, ...]:
        return self.__or__(other)

    def __and__(self, other: Date | tuple[date, ...]) -> tuple[date, ...]:
        if isinstance(other, Date):
            return tuple(sorted(set(self._date) & set(other._date)))
        elif isinstance(other, tuple):
            return tuple(sorted(set(self._date) & set(other)))
        raise TypeError("Invalid type.")

    def __rand__(self, other: Date | tuple[date, ...]) -> tuple[date, ...]:
        return self.__and__(other)

    def __contains__(self, other: Date | date) -> bool:
        if isinstance(other, Date):
            if not other.is_single_day:
                raise ValueError("Date object must represent a single day.")
            return other.dates[0] in self._date
        elif isinstance(other, date):
            return other in self._date
        else:
            raise TypeError("Invalid type.")

    def __matmul__(self, other: Date | date) -> Date:
        if not self.is_single_day:
            raise ValueError("Date object must represent a single day.")
        if isinstance(other, Date):
            if not other.is_single_day:
                raise ValueError("Date object must represent a single day.")
            other = other.first
        left = self._date[0].strftime("%m-%d-%Y")
        right = other.strftime("%m-%d-%Y")
        return Date(f"{left} ~ {right}")

    def __rmatmul__(self, other: Date | date) -> Date:
        if isinstance(other, date):
            other = Date(other)
        return other.__matmul__(self)

    @property
    def is_const(self) -> bool:
        return "*" not in self._expr and "~" not in self._expr

    @property
    def is_single_day(self) -> bool:
        return len(self._date) == 1

    @property
    def is_continuous(self) -> bool:
        for i in range(len(self._date) - 1):
            if self._date[i] + timedelta(days=1) != self._date[i + 1]:
                return False
        return True

    @property
    def length(self) -> int:
        return len(self._date)

    @property
    def dates(self) -> tuple[date, ...]:
        return self._date

    @property
    def first(self) -> date:
        return self._date[0]

    @property
    def last(self) -> date:
        return self._date[-1]
