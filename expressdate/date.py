from datetime import date, timedelta
from .parse import DateParser

__all__ = ["Date"]


class Date:
    """
    A Date object that can be instantiated from a Python datetime.date 
    or a string expression. 
    It supports various arithmetic, set-like, and logical operations 
    for date manipulation and comparison.
    """

    def __init__(self, expr: date | str):
        """
        Initialize the Date object.

        :param expr: A date object or a string representing a date or range.
        :raises TypeError: If expr is neither a date nor a string.
        """
        if isinstance(expr, str):
            # Store the original expression
            self._expr = expr
            # Parse the string into one or more dates
            self._date = DateParser.parse(expr)
        elif isinstance(expr, date):
            # Convert the date to a string in MM-DD-YYYY format
            self._expr = expr.strftime("%m-%d-%Y")
            # Store the single date in a tuple
            self._date = (expr,)
        else:
            raise TypeError("Invalid type.")

    def __hash__(self) -> int:
        """
        Return a hash based on the stored dates (tuple).

        :return: Hash value of the internal dates tuple.
        """
        return hash(self._date)

    def __str__(self) -> str:
        """
        Return a string representation of the date expression.

        :return: The original date expression as a string.
        """
        return self._expr

    def __repr__(self) -> str:
        """
        Return the official string representation of the Date object.

        :return: A string in the form of Date('MM-DD-YYYY') or equivalent.
        """
        return f"Date('{self._expr}')"

    def __add__(self, other: timedelta | int) -> tuple[date, ...]:
        """
        Add a timedelta or an integer number of days to each date in this Date.

        :param other: A timedelta object or an integer (representing days).
        :return: A tuple of date objects after addition.
        """
        if isinstance(other, int):
            # Convert an integer to timedelta days
            other = timedelta(days=other)
        # Add the timedelta to each date in the internal tuple
        return tuple(i + other for i in self._date)

    def __radd__(self, other: timedelta) -> tuple[date, ...]:
        """
        Reflective addition, allows adding dates to timedeltas.

        :param other: A timedelta object.
        :return: A tuple of date objects after addition.
        """
        return self.__add__(other)

    def __sub__(self, other: "Date" | tuple[date, ...]) -> tuple[date, ...]:
        """
        Subtract another Date object or a tuple of dates from this Date object.

        :param other: Another Date object or a tuple of date objects.
        :return: A tuple of date objects that are left after subtraction.
        :raises TypeError: If other is neither a Date nor a tuple of dates.
        """
        if isinstance(other, Date):
            return tuple(sorted(set(self._date) - set(other.dates)))
        elif isinstance(other, tuple):
            return tuple(sorted(set(self._date) - set(other)))
        raise TypeError("Invalid type.")

    def __rsub__(self, other: "Date" | tuple[date, ...]) -> tuple[date, ...]:
        """
        Reflective subtraction, subtracts this Date object 
        from another Date object or tuple of dates.

        :param other: Another Date object or a tuple of date objects.
        :return: A tuple of date objects that are left after subtraction.
        :raises TypeError: If other is neither a Date nor a tuple of dates.
        """
        if isinstance(other, Date):
            return tuple(sorted(set(other.dates) - set(self._date)))
        elif isinstance(other, tuple):
            return tuple(sorted(set(other) - set(self._date)))
        raise TypeError("Invalid type.")

    def __xor__(self, other: "Date" | tuple[date, ...]) -> tuple[date, ...]:
        """
        Perform a symmetric difference (XOR) between this Date object 
        and another Date object or tuple of dates.

        :param other: Another Date object or a tuple of date objects.
        :return: A tuple containing the symmetric difference of 
                 the two sets of dates.
        :raises TypeError: If other is an unsupported type.
        """
        if isinstance(other, Date):
            return tuple(sorted(set(self._date) ^ set(other._date)))
        elif isinstance(other, tuple):
            return tuple(sorted(set(self._date) ^ set(other)))
        raise TypeError("Invalid type.")

    def __rxor__(self, other: "Date" | tuple[date, ...]) -> tuple[date, ...]:
        """
        Reflective XOR, allows the other operand to be first 
        in a symmetric difference operation.

        :param other: Another Date object or a tuple of dates.
        :return: A tuple containing the symmetric difference of 
                 the two sets of dates.
        :raises TypeError: If other is an unsupported type.
        """
        if isinstance(other, Date):
            return tuple(sorted(set(other.dates) ^ set(self._date)))
        elif isinstance(other, tuple):
            return tuple(sorted(set(other) ^ set(self._date)))
        raise TypeError("Invalid type.")

    def __eq__(self, other: object) -> bool:
        """
        Check if this Date object is equal to another object.

        :param other: The object to compare against, can be Date, date, or str.
        :return: True if they are equal, False otherwise.
        """
        if isinstance(other, Date):
            return hash(self) == hash(other)
        elif isinstance(other, date):
            return self._date == (other,)
        elif isinstance(other, str):
            return hash(self) == hash(Date(other))
        return False

    def __ne__(self, other: object) -> bool:
        """
        Check if this Date object is not equal to another object.

        :param other: The object to compare against.
        :return: True if they are not equal, False otherwise.
        """
        return not self.__eq__(other)

    def __or__(self, other: "Date" | tuple[date, ...]) -> tuple[date, ...]:
        """
        Perform a union operation (OR) between this Date object and 
        another Date object or tuple of dates.

        :param other: Another Date object or a tuple of date objects.
        :return: A tuple of dates containing all unique dates from both.
        :raises TypeError: If other is an unsupported type.
        """
        if isinstance(other, Date):
            return tuple(sorted(set(self._date) | set(other._date)))
        elif isinstance(other, tuple):
            return tuple(sorted(set(self._date) | set(other)))
        raise TypeError("Invalid type.")

    def __ror__(self, other: "Date" | tuple[date, ...]) -> tuple[date, ...]:
        """
        Reflective OR operation, allows the other operand to be first 
        in a union operation.

        :param other: Another Date object or a tuple of dates.
        :return: A tuple of dates containing all unique dates from both.
        """
        return self.__or__(other)

    def __and__(self, other: "Date" | tuple[date, ...]) -> tuple[date, ...]:
        """
        Perform an intersection (AND) between this Date object 
        and another Date object or tuple of dates.

        :param other: Another Date object or a tuple of date objects.
        :return: A tuple of dates that are common to both.
        :raises TypeError: If other is an unsupported type.
        """
        if isinstance(other, Date):
            return tuple(sorted(set(self._date) & set(other._date)))
        elif isinstance(other, tuple):
            return tuple(sorted(set(self._date) & set(other)))
        raise TypeError("Invalid type.")

    def __rand__(self, other: "Date" | tuple[date, ...]) -> tuple[date, ...]:
        """
        Reflective AND operation, allows the other operand to be first 
        in an intersection operation.

        :param other: Another Date object or a tuple of dates.
        :return: A tuple of dates that are common to both.
        """
        return self.__and__(other)

    def __contains__(self, other: "Date" | date) -> bool:
        """
        Check if a given date or a single-day Date object is 
        contained within this Date object.

        :param other: A Date (representing a single day) or a date object.
        :return: True if the date is found, False otherwise.
        :raises ValueError: If the other Date object does not represent a single day.
        :raises TypeError: If the other object is not of type Date or date.
        """
        if isinstance(other, Date):
            if not other.is_single_day:
                raise ValueError("Date object must represent a single day.")
            return other.dates[0] in self._date
        elif isinstance(other, date):
            return other in self._date
        else:
            raise TypeError("Invalid type.")

    def __matmul__(self, other: "Date" | date) -> "Date":
        """
        Use the @ operator to combine two single-day Date objects 
        (or a Date and a date) into a new Date
        that expresses a range as "MM-DD-YYYY ~ MM-DD-YYYY".

        :param other: Another Date object (single day) or a date object.
        :return: A new Date object representing the combined string range.
        :raises ValueError: If either Date object represents 
                            more than a single day.
        """
        if not self.is_single_day:
            raise ValueError("Date object must represent a single day.")
        if isinstance(other, Date):
            if not other.is_single_day:
                raise ValueError("Date object must represent a single day.")
            other = other.first
        left = self._date[0].strftime("%m-%d-%Y")
        right = other.strftime("%m-%d-%Y")
        return Date(f"{left} ~ {right}")

    def __rmatmul__(self, other: "Date" | date) -> "Date":
        """
        Reflective matmul (@) operation to allow the other operand to 
        appear on the left.

        :param other: Another Date object or a date object.
        :return: A new Date object that represents the combined string range.
        """
        if isinstance(other, date):
            other = Date(other)
        return other.__matmul__(self)

    @property
    def is_const(self) -> bool:
        """
        Check if the internal date expression contains 
        no wildcards or range characters.

        :return: True if the expression is constant (no '*' or '~'), 
                 False otherwise.
        """
        return "*" not in self._expr and "~" not in self._expr

    @property
    def is_single_day(self) -> bool:
        """
        Check if this Date object represents only one day.

        :return: True if it contains exactly one date, False otherwise.
        """
        return len(self._date) == 1

    @property
    def is_continuous(self) -> bool:
        """
        Check if the dates within this object form 
        a continuous sequence without gaps.

        :return: True if consecutive days form a continuous range, 
                 False otherwise.
        """
        for i in range(len(self._date) - 1):
            if self._date[i] + timedelta(days=1) != self._date[i + 1]:
                return False
        return True

    @property
    def length(self) -> int:
        """
        Get the number of date objects stored.

        :return: The number of dates in this object.
        """
        return len(self._date)

    @property
    def dates(self) -> tuple[date, ...]:
        """
        Access the internal tuple of date objects.

        :return: A tuple containing all date objects.
        """
        return self._date

    @property
    def first(self) -> date:
        """
        Get the first date in the stored tuple.

        :return: The earliest date in this object.
        """
        return self._date[0]

    @property
    def last(self) -> date:
        """
        Get the last date in the stored tuple.

        :return: The latest date in this object.
        """
        return self._date[-1]
