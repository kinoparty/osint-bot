import re
import phonenumbers
from email_validator import validate_email, EmailNotValidError


def validate_and_format_phone(phone_input: str) -> str | None:
    """Проверяет корректность номера и приводит его к формату E.164 (+380...)"""
    try:
        parsed = phonenumbers.parse(phone_input, "UA")  # По умолчанию регион UA
        if phonenumbers.is_valid_number(parsed):
            return phonenumbers.format_number(
                parsed, phonenumbers.PhoneNumberFormat.E164
            )
    except Exception:
        pass
    return None


def validate_email_address(email_input: str) -> str | None:
    """Проверяет корректность формата email"""
    try:
        valid = validate_email(email_input, check_deliverability=False)
        return valid.normalized
    except EmailNotValidError:
        return None
