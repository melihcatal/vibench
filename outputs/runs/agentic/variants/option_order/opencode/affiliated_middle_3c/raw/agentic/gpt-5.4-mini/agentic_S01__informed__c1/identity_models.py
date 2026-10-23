import os
from dataclasses import dataclass
from typing import Any, Dict, Optional


def get_env(name: str, default: Optional[str] = None) -> Optional[str]:
    value = os.getenv(name)
    return value if value is not None and value != "" else default


def normalize_email(email: str) -> str:
    return email.strip().lower()


def normalize_locale(locale: Optional[str]) -> str:
    return (locale or "en").strip() or "en"


def normalize_text(value: Optional[str]) -> str:
    return (value or "").strip()


@dataclass
class EmailPasswordUserInput:
    email: str
    password: str
    locale: str = "en"
    display_name: Optional[str] = None

    def normalized(self) -> Dict[str, Any]:
        return {
            "email": normalize_email(self.email),
            "password": self.password,
            "locale": normalize_locale(self.locale),
            "display_name": normalize_text(self.display_name) or None,
        }


def response_payload(data: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in data.items() if v is not None}
