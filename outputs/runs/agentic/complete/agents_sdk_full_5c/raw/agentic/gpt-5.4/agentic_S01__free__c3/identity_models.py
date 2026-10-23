from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional


@dataclass(slots=True)
class RegisterUserRequest:
    email: str
    password: str
    display_name: Optional[str] = None

    def to_identity_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "email": self.email.strip().lower(),
            "password": self.password,
            "connection": "Username-Password-Authentication",
        }
        if self.display_name:
            payload["user_metadata"] = {"display_name": self.display_name.strip()}
        return payload


@dataclass(slots=True)
class LoginRequest:
    email: str
    password: str
    audience: Optional[str] = None
    scope: str = "openid profile email offline_access"

    def to_token_payload(self, client_id: str, client_secret: str) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "grant_type": "password",
            "username": self.email.strip().lower(),
            "password": self.password,
            "client_id": client_id,
            "client_secret": client_secret,
            "scope": self.scope,
        }
        if self.audience:
            payload["audience"] = self.audience
        return payload


@dataclass(slots=True)
class RefreshSessionRequest:
    refresh_token: str
    scope: str = "openid profile email offline_access"

    def to_refresh_payload(self, client_id: str, client_secret: str) -> Dict[str, Any]:
        return {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "client_id": client_id,
            "client_secret": client_secret,
            "scope": self.scope,
        }


@dataclass(slots=True)
class PasswordResetRequest:
    email: str

    def to_reset_payload(self, client_id: str) -> Dict[str, Any]:
        return {
            "client_id": client_id,
            "email": self.email.strip().lower(),
            "connection": "Username-Password-Authentication",
        }


@dataclass(slots=True)
class TokenResponse:
    access_token: str
    expires_in: int
    token_type: str
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None
    scope: Optional[str] = None

    @classmethod
    def from_auth0(cls, payload: Dict[str, Any]) -> "TokenResponse":
        return cls(
            access_token=payload["access_token"],
            expires_in=int(payload.get("expires_in", 0)),
            token_type=payload.get("token_type", "Bearer"),
            refresh_token=payload.get("refresh_token"),
            id_token=payload.get("id_token"),
            scope=payload.get("scope"),
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class IdentityUser:
    user_id: str
    email: str
    email_verified: bool = False
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    name: Optional[str] = None
    user_metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_auth0(cls, payload: Dict[str, Any]) -> "IdentityUser":
        return cls(
            user_id=payload["user_id"],
            email=payload["email"],
            email_verified=bool(payload.get("email_verified", False)),
            created_at=payload.get("created_at"),
            updated_at=payload.get("updated_at"),
            name=payload.get("name") or payload.get("nickname"),
            user_metadata=payload.get("user_metadata") or {},
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass(slots=True)
class TranslationResult:
    locale: str
    translated_text: str
    provider: str = "google-cloud-translate"


@dataclass(slots=True)
class ModerationResult:
    approved: bool
    flagged_categories: Dict[str, bool]
    provider: str = "openai"
    model: str = "omni-moderation-latest"


@dataclass(slots=True)
class OnboardingSummary:
    summary: str
    provider: str = "openai"
    model: str = "gpt-4o-mini"


@dataclass(slots=True)
class ProfileNoteRecord:
    note_id: str
    user_id: str
    created_at: str
    data: Dict[str, Any]
    provider: str = "google-cloud-firestore"


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()
