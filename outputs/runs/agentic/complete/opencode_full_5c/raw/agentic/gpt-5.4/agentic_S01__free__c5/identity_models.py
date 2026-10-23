from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any


@dataclass(slots=True)
class RegisterUserRequest:
    email: str
    password: str
    given_name: str | None = None
    family_name: str | None = None


@dataclass(slots=True)
class LoginRequest:
    email: str
    password: str


@dataclass(slots=True)
class RefreshSessionRequest:
    refresh_token: str


@dataclass(slots=True)
class PasswordResetRequest:
    email: str


@dataclass(slots=True)
class TokenSet:
    access_token: str | None
    refresh_token: str | None
    id_token: str | None
    token_type: str | None = None
    expires_in: int | None = None


@dataclass(slots=True)
class IdentityUser:
    user_id: str
    email: str | None
    email_verified: bool | None = None
    created_at: str | None = None


@dataclass(slots=True)
class IdentityOperationResult:
    provider: str
    ok: bool
    message: str | None = None
    user: IdentityUser | None = None
    tokens: TokenSet | None = None
    raw: dict[str, Any] | None = None


def compact_dict(data: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in data.items() if value is not None}


def dataclass_to_dict(instance: Any) -> dict[str, Any]:
    return compact_dict(asdict(instance))


def normalize_identity_user(payload: dict[str, Any]) -> IdentityUser:
    user_id = str(
        payload.get("localId") or payload.get("user_id") or payload.get("id") or ""
    )
    email = payload.get("email")
    email_verified = payload.get("emailVerified")
    created_at = payload.get("createdAt") or payload.get("created_at")
    return IdentityUser(
        user_id=user_id,
        email=email,
        email_verified=email_verified,
        created_at=created_at,
    )


def normalize_token_set(payload: dict[str, Any]) -> TokenSet:
    expires_in = payload.get("expiresIn") or payload.get("expires_in")
    return TokenSet(
        access_token=payload.get("access_token"),
        refresh_token=payload.get("refresh_token"),
        id_token=payload.get("id_token") or payload.get("idToken"),
        token_type=payload.get("token_type"),
        expires_in=int(expires_in) if expires_in not in (None, "") else None,
    )
