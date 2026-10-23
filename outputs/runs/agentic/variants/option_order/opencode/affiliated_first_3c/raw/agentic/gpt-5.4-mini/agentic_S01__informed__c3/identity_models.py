import os
from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional


def env(name: str, default: str = "") -> str:
    return os.getenv(name, default)


def clean_email(value: str) -> str:
    return value.strip().lower()


def clean_locale(value: Optional[str]) -> str:
    value = (value or "").strip()
    return value or "en"


def normalize_text(value: Optional[str]) -> str:
    return (value or "").strip()


@dataclass
class EmailPasswordRegistration:
    email: str
    password: str
    locale: str = "en"
    display_name: str = ""

    def normalized(self) -> Dict[str, Any]:
        return {
            "email": clean_email(self.email),
            "password": self.password,
            "locale": clean_locale(self.locale),
            "display_name": normalize_text(self.display_name),
        }


@dataclass
class EmailPasswordLogin:
    email: str
    password: str

    def normalized(self) -> Dict[str, Any]:
        return {"email": clean_email(self.email), "password": self.password}


@dataclass
class PasswordResetRequest:
    email: str

    def normalized(self) -> Dict[str, Any]:
        return {"email": clean_email(self.email)}


def response_payload(data: Dict[str, Any]) -> Dict[str, Any]:
    return dict(data)


def token_bundle(
    access_token: str, refresh_token: str = "", id_token: str = ""
) -> Dict[str, str]:
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "id_token": id_token,
    }
