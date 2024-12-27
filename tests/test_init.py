import pytest
from datetime import date
from expressdate import express


def test_express():
    d = express("2024-08-15")
    assert d.first == date(2024, 8, 15)
    d = express("2024-08-10 ~ 2024-08-15")
    assert d.dates == (
        date(2024, 8, 10),
        date(2024, 8, 11),
        date(2024, 8, 12),
        date(2024, 8, 13),
        date(2024, 8, 14),
        date(2024, 8, 15)
    )
    d = express("2024-08-1*")
    assert d.dates == (
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
    with pytest.raises(ValueError):
        express("2024-08-15 ~ 2024-08-10")
    with pytest.raises(ValueError):
        express("2024-08-10 ~ 2024-08-12 ~ 2024-08-14")
    with pytest.raises(ValueError):
        express("2024-08-1* ~ 2024-08-2*")
