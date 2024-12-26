from turtledemo.forest import doit2

import pytest
from datetime import date, timedelta
from expressdate.date import ExpressDate


def test_init():
    # Initialize with string
    d = ExpressDate("2024-08-15")
    assert d.first == date(2024, 8, 15)
    d = ExpressDate("2024-08-1*")
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
    # Initialize with date
    d = ExpressDate(date(2024, 8, 15))
    assert d.first == date(2024, 8, 15)
    # Test exceptions
    with pytest.raises(TypeError):
        # noinspection PyTypeChecker
        ExpressDate(20240815)  # pyright: ignore [reportArgumentType]
    


def test_hash():
    d1 = ExpressDate("2024-08-15")
    d2 = ExpressDate(date(2024, 8, 15))
    assert hash(d1) == hash(d2)


def test_str():
    expr = "2024-08-15"
    d = ExpressDate(expr)
    assert str(d) == expr


def test_repr():
    expr = "2024-08-15"
    d = ExpressDate(expr)
    assert repr(d) == f"ExpressDate('{expr}')"


def test_add():
    # Add timedelta
    d = ExpressDate("2024-08-15")
    result = d + timedelta(days=1)
    assert result[0] == date(2024, 8, 16)
    d = ExpressDate("2024-08-15 ~ 2024-08-17")
    result = d + timedelta(days=1)
    assert result == (
        date(2024, 8, 16),
        date(2024, 8, 17),
        date(2024, 8, 18)
    )
    # Add int
    d = ExpressDate("2024-08-15")
    result = d + 2
    assert result[0] == date(2024, 8, 17)
    d = ExpressDate("2024-08-15 ~ 2024-08-17")
    result = d + 2
    assert result == (
        date(2024, 8, 17),
        date(2024, 8, 18),
        date(2024, 8, 19)
    )


def test_radd():
    # Add timedelta
    d = ExpressDate("2024-08-15")
    result = timedelta(days=1) + d
    assert result[0] == date(2024, 8, 16)
    d = ExpressDate("2024-08-15 ~ 2024-08-17")
    result = timedelta(days=1) + d
    assert result == (
        date(2024, 8, 16),
        date(2024, 8, 17),
        date(2024, 8, 18)
    )


def test_sub():
    # Sub ExpressDate
    d1 = ExpressDate("2024-08-1*")
    d2 = ExpressDate("2024-08-10 ~ 2024-08-15")
    result = d1 - d2
    assert result == (
        date(2024, 8, 16),
        date(2024, 8, 17),
        date(2024, 8, 18),
        date(2024, 8, 19)
    )
    # Sub tuple
    d1 = ExpressDate("2024-08-1*")
    d2 = (
        date(2024, 8, 10),
        date(2024, 8, 11),
        date(2024, 8, 12),
        date(2024, 8, 13),
        date(2024, 8, 14),
        date(2024, 8, 15)
    )
    result = d1 - d2
    assert result == (
        date(2024, 8, 16),
        date(2024, 8, 17),
        date(2024, 8, 18),
        date(2024, 8, 19)
    )
    # Sub str
    d1 = ExpressDate("2024-08-1*")
    d2 = "2024-08-10 ~ 2024-08-15"
    result = d1 - d2
    assert result == (
        date(2024, 8, 16),
        date(2024, 8, 17),
        date(2024, 8, 18),
        date(2024, 8, 19)
    )


def test_rsub():
    # Sub tuple
    d1 = ExpressDate("2024-08-10 ~ 2024-08-15")
    d2 = (
        date(2024, 8, 10),
        date(2024, 8, 11),
        date(2024, 8, 12),
        date(2024, 8, 13),
        date(2024, 8, 14),
        date(2024, 8, 15),
        date(2024, 8, 16),
        date(2024, 8, 17),
        date(2024, 8, 18),
        date(2024, 8, 19),
    )
    result = d2 - d1
    assert result == (
        date(2024, 8, 16),
        date(2024, 8, 17),
        date(2024, 8, 18),
        date(2024, 8, 19)
    )
    # Sub tuple
    d1 = ExpressDate("2024-08-10 ~ 2024-08-15")
    d2 = "2024-08-1*"
    result = d2 - d1
    assert result == (
        date(2024, 8, 16),
        date(2024, 8, 17),
        date(2024, 8, 18),
        date(2024, 8, 19)
    )


def test_eq():
    # Compare ExpressDate and ExpressDate
    d1 = ExpressDate("2024-08-15")
    d2 = ExpressDate("2024-08-15")
    assert d1 == d2
    # Compare ExpressDate and datetime.date
    d1 = ExpressDate("2024-08-15")
    d2 = date(2024, 8, 15)
    assert d1 == d2
    # Compare ExpressDate and str
    d1 = ExpressDate("2024-08-1*")
    d2 = "2024-08-10 ~ 2024-08-19"
    assert d1 == d2
    # Test fail
    d1 = ExpressDate("2024-08-15")
    d2 = 20240815
    assert not d1 == d2


def test_ne():
    # Compare ExpressDate and ExpressDate
    d1 = ExpressDate("2024-08-15")
    d2 = ExpressDate("2024-08-16")
    assert d1 != d2
    # Compare ExpressDate and datetime.date
    d1 = ExpressDate("2024-08-15")
    d2 = date(2024, 8, 16)
    assert d1 != d2
    # Compare ExpressDate and str
    d1 = ExpressDate("2024-08-2*")
    d2 = "2024-08-10 ~ 2024-08-19"
    assert d1 != d2


def test_or():
    # Union ExpressDate and ExpressDate
    d1 = ExpressDate("2024-08-10 ~ 2024-08-16")
    d2 = ExpressDate("2024-08-14 ~ 2024-08-19")
    result = d1 | d2
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
        date(2024, 8, 19),
    )
    # Union ExpressDate and tuple
    d1 = ExpressDate("2024-08-10 ~ 2024-08-16")
    d2 = (
        date(2024, 8, 14),
        date(2024, 8, 15),
        date(2024, 8, 16),
        date(2024, 8, 17),
        date(2024, 8, 18),
        date(2024, 8, 19),
    )
    result = d1 | d2
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
        date(2024, 8, 19),
    )
    # Union ExpressDate and str
    d1 = ExpressDate("2024-08-10 ~ 2024-08-16")
    d2 = "2024-08-14 ~ 2024-08-19"
    result = d1 | d2
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
        date(2024, 8, 19),
    )


def test_ror():
    # Union tuple and ExpressDate
    d1 = ExpressDate("2024-08-14 ~ 2024-08-19")
    d2 = (
        date(2024, 8, 10),
        date(2024, 8, 11),
        date(2024, 8, 12),
        date(2024, 8, 13),
        date(2024, 8, 14),
        date(2024, 8, 15),
        date(2024, 8, 16),
    )
    result = d2 | d1
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
        date(2024, 8, 19),
    )
    # Union str and ExpressDate
    d1 = ExpressDate("2024-08-14 ~ 2024-08-19")
    d2 = "2024-08-10 ~ 2024-08-16"
    result = d2 | d1
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
        date(2024, 8, 19),
    )


def test_and():
    # Intersection ExpressDate and ExpressDate
    d1 = ExpressDate("2024-08-10 ~ 2024-08-16")
    d2 = ExpressDate("2024-08-14 ~ 2024-08-19")
    result = d1 & d2
    assert result == (
        date(2024, 8, 14),
        date(2024, 8, 15),
        date(2024, 8, 16),
    )
    # Intersection ExpressDate and tuple
    d1 = ExpressDate("2024-08-10 ~ 2024-08-16")
    d2 = (
        date(2024, 8, 14),
        date(2024, 8, 15),
        date(2024, 8, 16),
        date(2024, 8, 17),
        date(2024, 8, 18),
        date(2024, 8, 19),
    )
    result = d1 & d2
    assert result == (
        date(2024, 8, 14),
        date(2024, 8, 15),
        date(2024, 8, 16),
    )
    # Intersection ExpressDate and str
    d1 = ExpressDate("2024-08-10 ~ 2024-08-16")
    d2 = "2024-08-14 ~ 2024-08-19"
    result = d1 & d2
    assert result == (
        date(2024, 8, 14),
        date(2024, 8, 15),
        date(2024, 8, 16),
    )


def test_rand():
    # Intersection tuple and ExpressDate
    d1 = ExpressDate("2024-08-14 ~ 2024-08-19")
    d2 = (
        date(2024, 8, 10),
        date(2024, 8, 11),
        date(2024, 8, 12),
        date(2024, 8, 13),
        date(2024, 8, 14),
        date(2024, 8, 15),
        date(2024, 8, 16),
    )
    result = d2 & d1
    assert result == (
        date(2024, 8, 14),
        date(2024, 8, 15),
        date(2024, 8, 16),
    )
    # Intersection str and ExpressDate
    d1 = ExpressDate("2024-08-14 ~ 2024-08-19")
    d2 = "2024-08-10 ~ 2024-08-16"
    result = d2 & d1
    assert result == (
        date(2024, 8, 14),
        date(2024, 8, 15),
        date(2024, 8, 16),
    )


def test_xor():
    # Symmetric difference ExpressDate and ExpressDate
    d1 = ExpressDate("2024-08-10 ~ 2024-08-16")
    d2 = ExpressDate("2024-08-14 ~ 2024-08-19")
    result = d1 ^ d2
    assert result == (
        date(2024, 8, 10),
        date(2024, 8, 11),
        date(2024, 8, 12),
        date(2024, 8, 13),
        date(2024, 8, 17),
        date(2024, 8, 18),
        date(2024, 8, 19),
    )
    # Symmetric difference ExpressDate and tuple
    d1 = ExpressDate("2024-08-10 ~ 2024-08-16")
    d2 = (
        date(2024, 8, 14),
        date(2024, 8, 15),
        date(2024, 8, 16),
        date(2024, 8, 17),
        date(2024, 8, 18),
        date(2024, 8, 19),
    )
    result = d1 ^ d2
    assert result == (
        date(2024, 8, 10),
        date(2024, 8, 11),
        date(2024, 8, 12),
        date(2024, 8, 13),
        date(2024, 8, 17),
        date(2024, 8, 18),
        date(2024, 8, 19),
    )
    # Symmetric difference ExpressDate and str
    d1 = ExpressDate("2024-08-10 ~ 2024-08-16")
    d2 = "2024-08-14 ~ 2024-08-19"
    result = d1 ^ d2
    assert result == (
        date(2024, 8, 10),
        date(2024, 8, 11),
        date(2024, 8, 12),
        date(2024, 8, 13),
        date(2024, 8, 17),
        date(2024, 8, 18),
        date(2024, 8, 19),
    )


def test_rxor():
    # Symmetric difference tuple and ExpressDate
    d1 = ExpressDate("2024-08-14 ~ 2024-08-19")
    d2 = (
        date(2024, 8, 10),
        date(2024, 8, 11),
        date(2024, 8, 12),
        date(2024, 8, 13),
        date(2024, 8, 14),
        date(2024, 8, 15),
        date(2024, 8, 16),
    )
    result = d2 ^ d1
    assert result == (
        date(2024, 8, 10),
        date(2024, 8, 11),
        date(2024, 8, 12),
        date(2024, 8, 13),
        date(2024, 8, 17),
        date(2024, 8, 18),
        date(2024, 8, 19),
    )
    # Symmetric difference str and ExpressDate
    d1 = ExpressDate("2024-08-14 ~ 2024-08-19")
    d2 = "2024-08-10 ~ 2024-08-16"
    result = d2 ^ d1
    assert result == (
        date(2024, 8, 10),
        date(2024, 8, 11),
        date(2024, 8, 12),
        date(2024, 8, 13),
        date(2024, 8, 17),
        date(2024, 8, 18),
        date(2024, 8, 19),
    )


def test_date_contains():
    # Check ExpressDate contains ExpressDate
    d1 = ExpressDate("2024-08-15")
    d2 = ExpressDate("2024-08-1*")
    assert d1 in d2
    # Check date contains ExpressDate
    d1 = date(2024, 8, 15)
    d2 = ExpressDate("2024-08-1*")
    assert d1 in d2
    # Check str contains ExpressDate
    d1 = "2024-08-15"
    d2 = ExpressDate("2024-08-1*")
    assert d1 in d2
    # Exceptions
    with pytest.raises(TypeError):
        d = ExpressDate("2024-08-1*")
        assert 1 in d  # pyright: ignore [reportOperatorIssue]
    with pytest.raises(ValueError):
        d1 = ExpressDate("2024-08-1*")
        d2 = ExpressDate("2024-08-**")
        assert d1 in d2


def test_matmul():
    # Matmul ExpressDate and ExpressDate
    d1 = ExpressDate("2024-08-14")
    d2 = ExpressDate("2024-08-16")
    result = d1 @ d2
    assert result.dates == (
        date(2024, 8, 14),
        date(2024, 8, 15),
        date(2024, 8, 16)
    )
    # Matmul ExpressDate and date
    d1 = ExpressDate("2024-08-14")
    d2 = date(2024, 8, 16)
    result = d1 @ d2
    assert result.dates == (
        date(2024, 8, 14),
        date(2024, 8, 15),
        date(2024, 8, 16)
    )
    # Matmul ExpressDate and str
    d1 = ExpressDate("2024-08-14")
    d2 = "2024-08-16"
    result = d1 @ d2
    assert result.dates == (
        date(2024, 8, 14),
        date(2024, 8, 15),
        date(2024, 8, 16)
    )
    # Test exceptions
    with pytest.raises(ValueError):
        d1 = ExpressDate("2024-08-1*")
        d2 = ExpressDate("2024-08-16")
        assert d1 @ d2 is not None
    with pytest.raises(ValueError):
        d1 = ExpressDate("2024-08-14")
        d2 = ExpressDate("2024-08-1*")
        assert d1 @ d2 is not None
    
    
def test_rmatmul():
    # Matmul ExpressDate and date
    d1 = ExpressDate("2024-08-16")
    d2 = date(2024, 8, 14)
    result = d2 @ d1
    assert result.dates == (
        date(2024, 8, 14),
        date(2024, 8, 15),
        date(2024, 8, 16)
    )
    # Matmul ExpressDate and str
    d1 = ExpressDate("2024-08-16")
    d2 = "2024-08-14"
    result = d2 @ d1
    assert result.dates == (
        date(2024, 8, 14),
        date(2024, 8, 15),
        date(2024, 8, 16)
    )
    # Test exceptions
    with pytest.raises(ValueError):
        d1 = ExpressDate("2024-08-16")
        d2 = "2024-08-1*"
        assert d2 @ d1 is not None
    with pytest.raises(ValueError):
        d1 = ExpressDate("2024-08-1*")
        d2 = "2024-08-14"
        assert d2 @ d1 is not None
        
        
def test_is_const():
    assert ExpressDate("2024-08-15").is_const is True
    assert ExpressDate("2024-08-1*").is_const is False


def test_is_single_day():
    assert ExpressDate("2024-08-15").is_single_day is True
    assert ExpressDate("2024-08-1*").is_single_day is False


def test_is_continuous():
    assert ExpressDate("2024-08-1*").is_continuous is True
    assert ExpressDate("2024-08-*0").is_continuous is False
    
    
def test_length():
    assert ExpressDate("2024-08-1*").length == 10
    assert ExpressDate("2024-**-**").length == 366
    
    
def test_dates():
    assert ExpressDate("2024-08-1*").dates == (
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
    

def test_first():
    assert ExpressDate("2024-08-1*").first == date(2024, 8, 10)


def test_last():
    assert ExpressDate("2024-08-1*").last == date(2024, 8, 19)
