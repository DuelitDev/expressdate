from datetime import date, datetime, timedelta, tzinfo


class DateParser:
    @classmethod
    def parse(cls, expr: str, tz: tzinfo | None = None) -> tuple[date, ...]:
        # Parse a date or date range expression (expr).
        # If the expression does not contain a tilde (~), treat it as a single date.
        if "~" not in expr:
            return cls.parse_date(expr)

        # Handle date range expressions (e.g., "2023-01-01 ~ 2023-01-10").
        tilde_pos = expr.find("~")
        left = expr[:tilde_pos].strip()  # Extract the left side of the range.
        right = expr[tilde_pos + 1:].strip()  # Extract the right side of the range.
        today = datetime.now(tz=tz).date()  # Use today's date if needed.

        # If the right side is empty, assume the range ends at today.
        if right == "" and left:
            return cls.parse_date_range(cls.parse_const_date(left), today)

        # If both sides are specified, parse them and generate the full date range.
        elif left and right:
            return cls.parse_date_range(
                cls.parse_const_date(left), cls.parse_const_date(right)
            )

        # Raise an error if the expression is invalid.
        raise ValueError("Invalid date expression.")

    @classmethod
    def parse_date_range(cls, left: date, right: date) -> tuple[date, ...]:
        # Generate a list of dates within the specified range [left, right].
        # Ensure the left date is not greater than the right date.
        if left > right:
            raise ValueError("Invalid date range.")

        # Create a list of dates by iterating from the left date to the right date.
        dates = []
        i = left
        while i <= right:
            dates.append(i)
            i += timedelta(days=1)  # Increment by one day.
        return tuple(dates)

    @classmethod
    def parse_date(cls, expr: str) -> tuple[date, ...]:
        # Parse a single date expression.
        # If the expression contains a wildcard (*), handle it as an expression date.
        if "*" in expr:
            return cls.parse_expr_date(expr)

        # Otherwise, treat it as a constant date and parse it directly.
        return (cls.parse_const_date(expr),)

    @classmethod
    def parse_expr_date(cls, expr: str) -> tuple[date, ...]:
        # If expression is in American format (mm-dd-yyyy), convert to CJK.
        expr = cls.convert_to_cjk_style(expr)

        # Initialize a variable to store the weekday (e.g., "mon", "tue"), if any.
        week = None

        # If there's a comma, extract the date part and the weekday part.
        # For example: "2023-01-01, mon".
        if (comma_pos := expr.find(",")) != -1:
            expr, week = expr[:comma_pos], expr[comma_pos + 1 :].strip().lower()

        # Prepare an empty list to store all possible dates.
        dates = []

        # We'll search for asterisks (*) in the string, which indicate wildcard positions.
        # 'i' will be set to each asterisk's position in turn.
        i = -1
        while (i := expr.find("*", i + 1)) != -1:
            # Handle year-related wildcard positions (0~3).
            if 0 <= i < 3:
                # If the wildcard is among the first 3 digits of the year (e.g., "20*3"),
                # try replacing it with digits 0~9 to generate all possible years.
                for j in range(0, 10):
                    dates.extend(cls.parse_date(expr.replace("*", str(j), 1)))
                break
            if i == 3:
                # If the wildcard is the last digit of the year (e.g., "202*"),
                # still replace it with digits 0~9. If the first 3 digits are "000",
                # skip 0 because "0000" is typically invalid for years.
                for j in range(0 + (expr[0:3] == "000"), 10):
                    dates.extend(cls.parse_date(expr.replace("*", str(j), 1)))
                break

            # At this point, we know the year is fully determined.
            year = int(expr[:4])
            # Check if the determined year is a leap year.
            is_leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

            # Handle month-related wildcard positions (5~6).
            if i == 5:
                # If the wildcard is the tens digit of the month (e.g., "2023-*1-01"),
                # it could be 0 or 1 (up to '1' if the next digit is '0' to avoid invalid months).
                is_zero = expr[6] == "0"
                for j in range(0 + is_zero, 2):
                    dates.extend(cls.parse_date(expr.replace("*", str(j), 1)))
                break
            if i == 6:
                # If the wildcard is the ones digit of the month (e.g., "2023-0*-01"),
                # check if the tens digit is '1' which means the month could be 10, 11, or 12.
                is_over_ten = expr[5] == "1"
                for j in range(1 - is_over_ten, 3 if is_over_ten else 10):
                    dates.extend(cls.parse_date(expr.replace("*", str(j), 1)))
                break

            # At this point, we know the month is fully determined.
            month = int(expr[5:7])
            is_feb = month == 2

            # Handle day-related wildcard positions (8~9).
            if i == 8:
                # If the wildcard is the tens digit of the day (e.g., "2023-01-*1"),
                # we need to consider the validity based on whether it's Feb in a leap year, etc.
                is_zero = expr[9] == "0"
                # If the ones digit is greater than '8', we adapt the range in leap years.
                is_over_eight = expr[9] not in "*0" and expr[9] > "8"
                start = 0 + is_zero
                end = 3 - (is_over_eight and is_leap) if is_feb else 4 - is_zero
                for j in range(start, end):
                    dates.extend(cls.parse_date(expr.replace("*", str(j), 1)))
                break
            if i == 9:
                # If the wildcard is the ones digit of the day (e.g., "2023-01-1*"),
                # we consult an array that helps determine the maximum valid day based on the month.
                days_in_month = [2, 9 + is_leap, 2, 1, 2, 1, 2, 2, 1, 2, 1, 2]
                tens_digit = int(expr[8])
                start = 0 + (tens_digit == 0)
                if is_feb:
                    # If it's February, we check if tens_digit is 2 (for day 29 in leap years).
                    end = 10 if tens_digit != 2 else days_in_month[1]
                else:
                    # Otherwise, if tens_digit is 3, handle days 30 or 31 based on the month array.
                    end = 10 if tens_digit != 3 else days_in_month[month - 1]
                for j in range(start, end):
                    dates.append(cls.parse_const_date(expr.replace("*", str(j), 1)))
                break

        # If the weekday (like "mon", "tue", etc.) was specified,
        # filter the dates to keep only those weekdays.
        if week:
            tables = {
                "mon": 0,
                "tue": 1,
                "wed": 2,
                "thu": 3,
                "fri": 4,
                "sat": 5,
                "sun": 6,
            }
            temp = tables[week]
            return tuple(d for d in dates if d.weekday() == temp)

        # Return all generated dates if no weekday filtering is needed.
        return tuple(dates)

    @classmethod
    def parse_const_date(cls, expr: str) -> date:
        # If the expression is in CJK format, parse it using the appropriate date pattern.
        return datetime.strptime(cls.convert_to_cjk_style(expr), "%Y-%m-%d").date()

    @staticmethod
    def convert_to_cjk_style(expr: str) -> str:
        # Convert a date expression from American format (mm-dd-yyyy) to CJK format (yyyy-mm-dd).
        # The year is extracted from positions 6 onwards, the month from the first two characters,
        # and the day from positions 3 to 5.
        is_cjk_style = expr.find("-") == 4
        if not is_cjk_style:
            return f"{expr[6:]}-{expr[:2]}-{expr[3:5]}"
        return expr
