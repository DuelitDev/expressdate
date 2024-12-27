from .date import ExpressDate
from .parse import ExpressDateParser
from datetime import date

__all__ = ["express", "ExpressDate", "ExpressDateParser"]


def express(expr: date | str) -> ExpressDate:
    """
    Creates and returns a new ExpressDate object 
    from the provided date or string.

    :param expr: A Python date object or a string specifying one or more dates.
    :return: An ExpressDate instance representing the parsed date(s).
    """
    return ExpressDate(expr)
