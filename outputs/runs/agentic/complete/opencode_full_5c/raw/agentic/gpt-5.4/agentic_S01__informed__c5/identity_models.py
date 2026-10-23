from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def _clean_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in data.items() if v is not None}


@dataclass
class RegisterUserRequest:
    email: str
    password: str
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    name: Optional[str] = None
    user_metadata: Dict[str, Any] = field(default_factory=dict)

    def to_auth0_payload(self, connection: str) -> Dict[str, Any]:
        payload = {
            "connection": connection,
            "email": self.email,
            "password": self.password,
            "user_metadata": self.user_metadata or {},
        }
        if self.given_name:
            payload["given_name"] = self.given_name
        if self.family_name:
            payload["family_name"] = self.family_name
        if self.name:
            payload["name"] = self.name
        return payload


@dataclass
class LoginRequest:
    email: str
    password: str
    audience: Optional[str] = None
    scope: str = "openid profile email offline_access"

    def to_auth0_payload(self, client_id: str, client_secret: str) -> Dict[str, Any]:
        return _clean_dict(
            {
                "grant_type": "password",
                "username": self.email,
                "password": self.password,
                "scope": self.scope,
                "audience": self.audience,
                "client_id": client_id,
                "client_secret": client_secret,
            }
        )


@dataclass
class RefreshSessionRequest:
    refresh_token: str
    scope: str = "openid profile email offline_access"

    def to_auth0_payload(self, client_id: str, client_secret: str) -> Dict[str, Any]:
        return {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "scope": self.scope,
            "client_id": client_id,
            "client_secret": client_secret,
        }


@dataclass
class PasswordResetRequest:
    email: str

    def to_auth0_payload(self, client_id: str, connection: str) -> Dict[str, Any]:
        return {
            "client_id": client_id,
            "email": self.email,
            "connection": connection,
        }


@dataclass
class TokenResponse:
    access_token: str
    expires_in: int
    token_type: str
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None
    scope: Optional[str] = None

    @classmethod
    def from_auth0(cls, data: Dict[str, Any]) -> "TokenResponse":
        return cls(
            access_token=data["access_token"],
            expires_in=int(data.get("expires_in", 0)),
            token_type=data.get("token_type", "Bearer"),
            refresh_token=data.get("refresh_token"),
            id_token=data.get("id_token"),
            scope=data.get("scope"),
        )


@dataclass
class UserAccount:
    user_id: str
    email: str
    email_verified: bool
    created_at: Optional[str] = None
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    user_metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_auth0(cls, data: Dict[str, Any]) -> "UserAccount":
        return cls(
            user_id=data["user_id"],
            email=data["email"],
            email_verified=bool(data.get("email_verified", False)),
            created_at=data.get("created_at"),
            name=data.get("name"),
            given_name=data.get("given_name"),
            family_name=data.get("family_name"),
            user_metadata=data.get("user_metadata") or {},
        )


@dataclass
class TranslationResult:
    locale: str
    translated_text: str
    provider: str = "deepl"
    model: Optional[str] = None


@dataclass
class ModerationResult:
    provider: str
    flagged: bool
    scores: Dict[str, float]
    allowed: bool
    flagged_categories: List[str] = field(default_factory=list)


@dataclass
class OnboardingSummary:
    user_id: str
    locale: str
    summary: str
    provider: str
    model: str


@dataclass
class ProfileNoteRecord:
    user_id: str
    note_id: str
    note: str
    support_metadata: Dict[str, Any]
    created_at: str

    def to_document(self) -> Dict[str, Any]:
        return {
            "_id": self.note_id,
            "user_id": self.user_id,
            "note": self.note,
            "support_metadata": self.support_metadata,
            "created_at": self.created_at,
        }
