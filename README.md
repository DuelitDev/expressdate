# expressdate

![](https://github.com/DuelitDev/expressdate/actions/workflows/ci.yml/badge.svg)
[![codecov](https://codecov.io/github/DuelitDev/expressdate/graph/badge.svg?token=794OKQP8KS)](https://codecov.io/github/DuelitDev/expressdate)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/expressdate)](https://pypistats.org/packages/expressdate/)

---

# Install
```shell
pip install -U expressdate
```

# Key Features
- Intuitive Date and Range Expressions
- Relative Date Handling and Flexible Conversion

---
# Getting Started
```python
import expressdate


date = expressdate.expr("2024-08-15")
print(date.first)          # 2024-08-15
print(date.is_single_day)  # True

date = expressdate.expr("2024-08-10 ~ 2024-08-15")
print(date.dates)          # 2024-08-10 ~ 2024-08-15
print(date.is_single_day)  # False

date = expressdate.expr("2024-08-1*")
print(date.dates)          # 2024-08-10 ~ 2024-08-19
print(date.is_continuous)  # True

date = expressdate.expr("2024-08-2*, Tue")
print(date.dates)          # 2024-08-20, 2024-08-27
print(date.is_continuous)  # False

# don't do this. It takes very long time.
# This creates 3,652,059 `datetime.date` objects.
date = expressdate.expr("****-**-**")
print(date.dates)  # 0001-01-01 ~ 9999-12-31
```

---

# Documentation
https://github.com/DueltiDev/expressdate/wiki

---

# Requirements
- python 3.10 or higher

---

# License
`expressdate` is offered under the MIT license.


