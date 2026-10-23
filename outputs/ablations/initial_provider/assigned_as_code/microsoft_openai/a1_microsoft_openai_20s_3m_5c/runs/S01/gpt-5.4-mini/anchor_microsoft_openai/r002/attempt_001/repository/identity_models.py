from dataclasses import dataclass


def normalize_email(email):
    return email.strip().lower()


def normalize_locale(locale):
    return (locale or 'en').replace('_', '-').lower()


def require_fields(payload, fields):
    missing = [field for field in fields if field not in payload or payload[field] in (None, '')]
    if missing:
        raise ValueError('missing_fields:' + ','.join(missing))
    return payload


@dataclass
class AccountRequest:
    email: str
    password: str


@dataclass
class LocaleRequest:
    text: str
    locale: str
