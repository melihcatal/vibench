from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class RegisterUserRequest:
    email: str
    password: str
    given_name: Optional[str] = None
    family_name: Optional[str] = None


@dataclass
class RegisterUserResponse:
    user_id: str
    email: str
    email_verified: bool
    provider: str
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LoginRequest:
    email: str
    password: str
    scope: str = "openid profile email offline_access"


@dataclass
class TokenBundle:
    access_token: str
    refresh_token: Optional[str]
    id_token: Optional[str]
    token_type: str
    expires_in: int
    scope: Optional[str]
    provider: str
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RefreshSessionRequest:
    refresh_token: str
    scope: str = "openid profile email offline_access"


@dataclass
class PasswordResetRequest:
    email: str
    connection: Optional[str] = None


@dataclass
class PasswordResetResponse:
    email: str
    initiated: bool
    provider: str
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TranslationRequest:
    text: str
    target_locale: str
    source_locale: Optional[str] = None


@dataclass
class ModerationRequest:
    profile_text: str


@dataclass
class SummaryRequest:
    onboarding_events: List[Dict[str, Any]]
    locale: Optional[str] = None


@dataclass
class ProfileNoteRecord:
    user_id: str
    note: str
    support_metadata: Dict[str, Any]


def to_payload(model: Any) -> Dict[str, Any]:
    return {key: value for key, value in asdict(model).items() if value is not None}


def normalize_auth0_user(payload: Dict[str, Any]) -> RegisterUserResponse:
    return RegisterUserResponse(
        user_id=payload.get("user_id", ""),
        email=payload.get("email", ""),
        email_verified=bool(payload.get("email_verified", False)),
        provider="auth0",
        raw=payload,
    )


def normalize_auth0_tokens(payload: Dict[str, Any]) -> TokenBundle:
    return TokenBundle(
        access_token=payload["access_token"],
        refresh_token=payload.get("refresh_token"),
        id_token=payload.get("id_token"),
        token_type=payload.get("token_type", "Bearer"),
        expires_in=int(payload.get("expires_in", 0)),
        scope=payload.get("scope"),
        provider="auth0",
        raw=payload,
    )


def normalize_password_reset(
    email: str, payload: Dict[str, Any]
) -> PasswordResetResponse:
    initiated = bool(payload) or payload == {}
    return PasswordResetResponse(
        email=email, initiated=initiated, provider="auth0", raw=payload
    )
