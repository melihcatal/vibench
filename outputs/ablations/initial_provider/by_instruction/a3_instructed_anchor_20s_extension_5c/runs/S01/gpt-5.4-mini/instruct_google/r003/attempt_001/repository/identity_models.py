from dataclasses import dataclass
from typing import Any, Dict, Optional


def normalize_email(email: str) -> str:
    return email.strip().lower()


def normalize_locale(locale: Optional[str]) -> str:
    return (locale or "en").strip() or "en"


@dataclass
class AccountCredentials:
    email: str
    password: str
    display_name: Optional[str] = None

    def normalized(self) -> "AccountCredentials":
        return AccountCredentials(
            email=normalize_email(self.email),
            password=self.password,
            display_name=self.display_name.strip() if self.display_name else None,
        )


@dataclass
class LoginResult:
    access_token: str
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None
    expires_in: Optional[int] = None
    raw: Optional[Dict[str, Any]] = None
