from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional


@dataclass(frozen=True)
class EmailPasswordRequest:
    email: str
    password: str


@dataclass(frozen=True)
class UserRegistrationRequest(EmailPasswordRequest):
    name: Optional[str] = None
    locale: Optional[str] = None


@dataclass(frozen=True)
class TokenResponse:
    access_token: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: str = "Bearer"
    expires_in: Optional[int] = None


@dataclass(frozen=True)
class PasswordResetRequest:
    email: str
    connection: Optional[str] = None


@dataclass(frozen=True)
class NormalizedIdentity:
    email: str
    password: Optional[str] = None
    name: Optional[str] = None
    locale: Optional[str] = None


def normalize_email(value: str) -> str:
    return value.strip().lower()


def normalize_registration(data: Dict[str, Any]) -> NormalizedIdentity:
    return NormalizedIdentity(
        email=normalize_email(data["email"]),
        password=data.get("password"),
        name=(data.get("name") or None),
        locale=(data.get("locale") or None),
    )


def as_payload(obj: Any) -> Dict[str, Any]:
    return {k: v for k, v in asdict(obj).items() if v is not None}
