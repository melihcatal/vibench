from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


@dataclass(slots=True)
class RegisterUserRequest:
    email: str
    password: str
    given_name: Optional[str] = None
    family_name: Optional[str] = None

    def to_auth0_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "email": self.email,
            "password": self.password,
            "connection": "Username-Password-Authentication",
        }
        if self.given_name or self.family_name:
            payload["user_metadata"] = {
                "given_name": self.given_name,
                "family_name": self.family_name,
            }
        return payload


@dataclass(slots=True)
class LoginRequest:
    email: str
    password: str
    audience: Optional[str] = None
    scope: str = "openid profile email offline_access"

    def to_auth0_payload(self, client_id: str, client_secret: str) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "grant_type": "password",
            "username": self.email,
            "password": self.password,
            "client_id": client_id,
            "client_secret": client_secret,
            "scope": self.scope,
        }
        if self.audience:
            payload["audience"] = self.audience
        return payload


@dataclass(slots=True)
class RefreshRequest:
    refresh_token: str
    scope: str = "openid profile email offline_access"

    def to_auth0_payload(self, client_id: str, client_secret: str) -> Dict[str, Any]:
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
    connection: str = "Username-Password-Authentication"

    def to_auth0_payload(self, client_id: str) -> Dict[str, Any]:
        return {
            "client_id": client_id,
            "email": self.email,
            "connection": self.connection,
        }


@dataclass(slots=True)
class TokenResponse:
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None
    scope: Optional[str] = None

    @classmethod
    def from_auth0(cls, payload: Dict[str, Any]) -> "TokenResponse":
        return cls(
            access_token=payload["access_token"],
            token_type=payload.get("token_type", "Bearer"),
            expires_in=int(payload.get("expires_in", 0)),
            refresh_token=payload.get("refresh_token"),
            id_token=payload.get("id_token"),
            scope=payload.get("scope"),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "access_token": self.access_token,
            "token_type": self.token_type,
            "expires_in": self.expires_in,
            "refresh_token": self.refresh_token,
            "id_token": self.id_token,
            "scope": self.scope,
        }


@dataclass(slots=True)
class UserRecord:
    user_id: str
    email: str
    email_verified: bool
    created_at: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_auth0(cls, payload: Dict[str, Any]) -> "UserRecord":
        return cls(
            user_id=payload["user_id"],
            email=payload["email"],
            email_verified=bool(payload.get("email_verified", False)),
            created_at=payload.get("created_at"),
            raw=payload,
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "email": self.email,
            "email_verified": self.email_verified,
            "created_at": self.created_at,
            "raw": self.raw,
        }


@dataclass(slots=True)
class TranslationResult:
    provider: str
    target_language: str
    translated_text: str
    detected_source_language: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "provider": self.provider,
            "target_language": self.target_language,
            "translated_text": self.translated_text,
            "detected_source_language": self.detected_source_language,
        }


@dataclass(slots=True)
class ModerationResult:
    provider: str
    approved: bool
    flagged_categories: List[str]
    scores: Dict[str, float]
    raw: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "provider": self.provider,
            "approved": self.approved,
            "flagged_categories": self.flagged_categories,
            "scores": self.scores,
            "raw": self.raw,
        }


@dataclass(slots=True)
class SummaryResult:
    provider: str
    model: str
    summary: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "provider": self.provider,
            "model": self.model,
            "summary": self.summary,
        }


@dataclass(slots=True)
class ProfileNote:
    user_id: str
    notes: str
    support_metadata: Dict[str, Any]
    locale: Optional[str] = None
    updated_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_document(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "notes": self.notes,
            "support_metadata": self.support_metadata,
            "locale": self.locale,
            "updated_at": self.updated_at,
        }
