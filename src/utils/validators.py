"""Input validation helpers. Each returns (is_valid, error_message)."""
import re

EMAIL_PATTERN = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.-]+$")


def validate_name(name):
    if not name or not name.strip():
        return False, "Name cannot be empty."
    return True, ""


def validate_email(email):
    if not email or not EMAIL_PATTERN.match(email.strip()):
        return False, "Invalid email format."
    return True, ""


def validate_course(course):
    if not course or not course.strip():
        return False, "Course cannot be empty."
    return True, ""


def validate_year_level(year_level):
    try:
        year = int(year_level)
    except (TypeError, ValueError):
        return False, "Year level must be a number."
    if not 1 <= year <= 6:
        return False, "Year level must be between 1 and 6."
    return True, ""


def validate_gpa(gpa):
    try:
        value = float(gpa)
    except (TypeError, ValueError):
        return False, "GPA must be a number."
    if not 0.0 <= value <= 4.0:
        return False, "GPA must be between 0.0 and 4.0."
    return True, ""
