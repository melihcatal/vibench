from dataclasses import dataclass, field
from typing import Any, Mapping, Optional
import re


_EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


def normalize_email(email: str) -> str:
    value = str(email).strip().lower()
    if not value or not _EMAIL_RE.match(value):
        raise ValueError("invalid email")
    return value


def normalize_password(password: str) -> str:
    value = str(password)
    if not value:
        raise ValueError("password required")
    return value


def normalize_display_name(display_name: Optional[str]) -> Optional[str]:
    if display_name is None:
        return None
    value = str(display_name).strip()
    return value or None


def normalize_account_identifier(value: Any) -> str:
    if value is None:
        raise ValueError("account identifier required")
    text = str(value).strip()
    if not text:
        raise ValueError("account identifier required")
    return text


@dataclass(frozen=True)
class CreateAccountRequest:
    email: str
    password: str
    display_name: Optional[str] = None
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def normalized(self) -> "CreateAccountRequest":
        return CreateAccountRequest(
            email=normalize_email(self.email),
            password=normalize_password(self.password),
            display_name=normalize_display_name(self.display_name),
            metadata=dict(self.metadata),
        )


@dataclass(frozen=True)
class UpdatePasswordRequest:
    account_id: str
    current_password: str
    new_password: str

    def normalized(self) -> "UpdatePasswordRequest":
        return UpdatePasswordRequest(
            account_id=normalize_account_identifier(self.account_id),
            current_password=normalize_password(self.current_password),
            new_password=normalize_password(self.new_password),
        )


@dataclass(frozen=True)
class LoginRequest:
    email: str
    password: str

    def normalized(self) -> "LoginRequest":
        return LoginRequest(
            email=normalize_email(self.email),
            password=normalize_password(self.password),
        )


@dataclass(frozen=True)
class AccountResponse:
    account_id: str
    email: str
    display_name: Optional[str] = None
    is_active: bool = True
    email_verified: bool = False
    metadata: Mapping[str, Any] = field(default_factory=dict)

    def normalized(self) -> "AccountResponse":
        return AccountResponse(
            account_id=normalize_account_identifier(self.account_id),
            email=normalize_email(self.email),
            display_name=normalize_display_name(self.display_name),
            is_active=bool(self.is_active),
            email_verified=bool(self.email_verified),
            metadata=dict(self.metadata),
        )


@dataclass(frozen=True)
class TokenResponse:
    access_token: str
    token_type: str = "bearer"
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None

    def normalized(self) -> "TokenResponse":
        token_type = str(self.token_type).strip().lower() or "bearer"
        expires_in = None if self.expires_in is None else int(self.expires_in)
        return TokenResponse(
            access_token=str(self.access_token).strip(),
            token_type=token_type,
            refresh_token=None if self.refresh_token is None else str(self.refresh_token).strip() or None,
            expires_in=expires_in,
        )


def normalize_account_response(payload: Mapping[str, Any]) -> AccountResponse:
    return AccountResponse(
        account_id=payload.get("account_id", payload.get("id", "")),
        email=payload.get("email", ""),
        display_name=payload.get("display_name"),
        is_active=payload.get("is_active", True),
        email_verified=payload.get("email_verified", False),
        metadata=payload.get("metadata", {}),
    ).normalized()


def normalize_token_response(payload: Mapping[str, Any]) -> TokenResponse:
    return TokenResponse(
        access_token=payload.get("access_token", ""),
        token_type=payload.get("token_type", "bearer"),
        refresh_token=payload.get("refresh_token"),
        expires_in=payload.get("expires_in"),
    ).normalized()
