from dataclasses import dataclass
from email.utils import parseaddr
from typing import Any, Dict, Optional
import re


_EMAIL_LOCAL_RE = re.compile(r"^[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+$")
_EMAIL_DOMAIN_RE = re.compile(r"^(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?)(?:\.(?:[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?))*$")


def normalize_email(email: str) -> str:
    address = parseaddr((email or "").strip())[1].strip()
    if not address or "@" not in address:
        raise ValueError("invalid_email")
    local, domain = address.rsplit("@", 1)
    if not local or not domain:
        raise ValueError("invalid_email")
    local = local.strip()
    domain = domain.strip().lower()
    if not _EMAIL_LOCAL_RE.match(local) or not _EMAIL_DOMAIN_RE.match(domain):
        raise ValueError("invalid_email")
    return f"{local}@{domain}"


def normalize_password(password: str) -> str:
    password = (password or "").strip()
    if len(password) < 8:
        raise ValueError("password_too_short")
    return password


@dataclass(frozen=True)
class AccountCreateRequest:
    email: str
    password: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AccountCreateRequest":
        return cls(
            email=normalize_email(str(data.get("email", ""))),
            password=normalize_password(str(data.get("password", ""))),
        )


@dataclass(frozen=True)
class AccountLoginRequest:
    email: str
    password: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AccountLoginRequest":
        return cls(
            email=normalize_email(str(data.get("email", ""))),
            password=normalize_password(str(data.get("password", ""))),
        )


@dataclass(frozen=True)
class AccountUpdatePasswordRequest:
    email: str
    current_password: str
    new_password: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AccountUpdatePasswordRequest":
        return cls(
            email=normalize_email(str(data.get("email", ""))),
            current_password=normalize_password(str(data.get("current_password", ""))),
            new_password=normalize_password(str(data.get("new_password", ""))),
        )


@dataclass(frozen=True)
class AccountDeleteRequest:
    email: str
    password: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AccountDeleteRequest":
        password = data.get("password")
        return cls(
            email=normalize_email(str(data.get("email", ""))),
            password=normalize_password(str(password)) if password is not None else None,
        )


@dataclass(frozen=True)
class AccountResponse:
    email: str
    status: str
    message: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AccountResponse":
        return cls(
            email=normalize_email(str(data.get("email", ""))),
            status=str(data.get("status", "")).strip().lower() or "unknown",
            message=str(data.get("message")).strip() if data.get("message") is not None else None,
        )
