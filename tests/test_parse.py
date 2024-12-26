import pytest
from datetime import date
from zoneinfo import ZoneInfo
from expressdate.parse import DateParser


def test_convert_to_cjk_conversion():
    result = DateParser.convert_to_cjk_style("08-15-2024")
    assert result == "2024-08-15"


def test_parse_const_date():
    # Test in CJK format
    result = DateParser.parse_const_date("2024-08-15")
    assert result == date(2024, 8, 15)
    # Test in american format
    result = DateParser.parse_const_date("08-15-2024")
    assert result == date(2024, 8, 15)


def test_parse_expr_date():
    # single day
    result = DateParser.parse_date("2024-08-15")
    assert result == (date(2024, 8, 15),)
    # 2024-08-10 ~ 2024-08-19
    result = DateParser.parse_expr_date("2024-08-1*")
    assert len(result) == 10
    assert result == (
        date(2024, 8, 10),
        date(2024, 8, 11),
        date(2024, 8, 12),
        date(2024, 8, 13),
        date(2024, 8, 14),
        date(2024, 8, 15),
        date(2024, 8, 16),
        date(2024, 8, 17),
        date(2024, 8, 18),
        date(2024, 8, 19)
    )
    # 2024-08-01 ~ 2024-08-31
    result = DateParser.parse_expr_date("2024-08-**")
    assert len(result) == 31
    assert date(2024, 8, 1) in result
    assert date(2024, 8, 31) in result
    # February test (a leap year)
    result = DateParser.parse_expr_date("2024-02-**")
    assert len(result) == 29
    assert date(2024, 2, 1) in result
    assert date(2024, 2, 29) in result
    # February test (not a leap year)
    result = DateParser.parse_expr_date("2023-02-**")
    assert len(result) == 28
    assert date(2023, 2, 1) in result
    assert date(2023, 2, 28) in result
    # Test a leap year.
    result = DateParser.parse_expr_date("2024-**-**")
    assert len(result) == 366
    # Test long range dates.
    result = DateParser.parse_expr_date("19**-**-10")
    assert len(result) == 1200
    assert date(1900, 1, 10) in result
    assert date(1999, 12, 10) in result
    # Test with week
    result = DateParser.parse_expr_date("2024-**-**, mon")
    assert len(result) == 53
    assert date(2024, 1, 1) in result  # It is monday.
    assert date(2024, 12, 31) not in result  # It is tuesday.


def test_parse_date_range():
    result = DateParser.parse_date_range(date(2024, 8, 15), date(2024, 8, 20))
    assert result == (
        date(2024, 8, 15),
        date(2024, 8, 16),
        date(2024, 8, 17),
        date(2024, 8, 18),
        date(2024, 8, 19),
        date(2024, 8, 20),
    )
    # auto fill
    today = date.today()
    result = DateParser.parse(f"{today} ~ ")
    assert result == (today,)
    # invaild order
    with pytest.raises(ValueError):
        DateParser.parse_date_range(date(2024, 8, 20), date(2024, 8, 15))


def test_parse():
    # single day
    result = DateParser.parse("2024-08-15")
    assert result == (date(2024, 8, 15),)
    # 2024-08-10 ~ 2024-08-19
    result = DateParser.parse("2024-08-1*")
    assert len(result) == 10
    assert result == (
        date(2024, 8, 10),
        date(2024, 8, 11),
        date(2024, 8, 12),
        date(2024, 8, 13),
        date(2024, 8, 14),
        date(2024, 8, 15),
        date(2024, 8, 16),
        date(2024, 8, 17),
        date(2024, 8, 18),
        date(2024, 8, 19)
    )
    # 2024-08-01 ~ 2024-08-31
    result = DateParser.parse("2024-08-**")
    assert len(result) == 31
    assert date(2024, 8, 1) in result
    assert date(2024, 8, 31) in result
    # February test (a leap year)
    result = DateParser.parse("2024-02-**")
    assert len(result) == 29
    assert date(2024, 2, 1) in result
    assert date(2024, 2, 29) in result
    # February test (not a leap year)
    result = DateParser.parse("2023-02-**")
    assert len(result) == 28
    assert date(2023, 2, 1) in result
    assert date(2023, 2, 28) in result
    # Test a leap year.
    result = DateParser.parse("2024-**-**")
    assert len(result) == 366
    # Test long range dates.
    result = DateParser.parse("19**-**-10")
    assert len(result) == 1200
    assert date(1900, 1, 10) in result
    assert date(1999, 12, 10) in result
    # Test with week
    result = DateParser.parse("2024-**-**, mon")
    assert len(result) == 53
    assert date(2024, 1, 1) in result  # It is monday.
    assert date(2024, 12, 31) not in result  # It is tuesday.
    # Test with timezone info
    tz = ZoneInfo("America/New_York")
    result = DateParser.parse("2024-08-15", tz)
    assert result == (date(2024, 8, 15),)
    # Test range dates.
    result = DateParser.parse("2024-08-15 ~ 2024-08-20")
    assert result == (
        date(2024, 8, 15),
        date(2024, 8, 16),
        date(2024, 8, 17),
        date(2024, 8, 18),
        date(2024, 8, 19),
        date(2024, 8, 20)
    )
    # Test invalid order
    with pytest.raises(ValueError):
        DateParser.parse("2024-08-20 ~ 2024-08-15")
    with pytest.raises(ValueError):
        DateParser.parse("~ 2024-08-15")
    with pytest.raises(ValueError):
        DateParser.parse("Hello, World!")
