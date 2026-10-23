from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, Optional


@dataclass(slots=True)
class RegisterUserRequest:
    email: str
    password: str
    display_name: Optional[str] = None


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
class WelcomeTranslateRequest:
    text: str
    target_locale: str
    source_locale: Optional[str] = None


@dataclass(slots=True)
class ProfileModerationRequest:
    profile_text: str


@dataclass(slots=True)
class OnboardingSummaryRequest:
    onboarding_state: Dict[str, Any]


@dataclass(slots=True)
class ProfileNoteStoreRequest:
    user_id: str
    email: str
    notes: str
    metadata: Optional[Dict[str, Any]] = None


@dataclass(slots=True)
class AuthTokens:
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int
    id_token: Optional[str] = None


@dataclass(slots=True)
class IdentityUser:
    user_id: str
    email: str
    email_verified: bool
    display_name: Optional[str] = None


@dataclass(slots=True)
class StoredNote:
    document_id: str
    user_id: str
    email: str
    metadata: Dict[str, Any]


def model_to_dict(model: Any) -> Dict[str, Any]:
    return asdict(model)


def normalize_email(value: str) -> str:
    return value.strip().lower()


def normalize_supabase_user(payload: Dict[str, Any]) -> IdentityUser:
    user = payload.get("user") if "user" in payload else payload
    return IdentityUser(
        user_id=user["id"],
        email=user["email"],
        email_verified=bool(user.get("email_confirmed_at") or user.get("confirmed_at")),
        display_name=(user.get("user_metadata") or {}).get("display_name"),
    )


def normalize_supabase_tokens(payload: Dict[str, Any]) -> AuthTokens:
    return AuthTokens(
        access_token=payload["access_token"],
        refresh_token=payload["refresh_token"],
        token_type=payload.get("token_type", "bearer"),
        expires_in=int(payload.get("expires_in", 0)),
        id_token=payload.get("id_token"),
    )
