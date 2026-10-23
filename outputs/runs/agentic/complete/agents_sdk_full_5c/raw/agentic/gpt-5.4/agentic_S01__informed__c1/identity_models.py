from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class RegisterUserRequest:
    email: str
    password: str
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    email_verified: bool = False
    user_metadata: Dict[str, Any] = field(default_factory=dict)

    def to_auth0_payload(self, connection: str) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "connection": connection,
            "email": self.email,
            "password": self.password,
            "email_verified": self.email_verified,
        }
        if self.given_name:
            payload["given_name"] = self.given_name
        if self.family_name:
            payload["family_name"] = self.family_name
        if self.user_metadata:
            payload["user_metadata"] = self.user_metadata
        return payload


@dataclass
class LoginRequest:
    email: str
    password: str
    audience: Optional[str] = None
    scope: str = "openid profile email offline_access"

    def to_token_payload(self, client_id: str, client_secret: str) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "grant_type": "password",
            "username": self.email,
            "password": self.password,
            "scope": self.scope,
            "client_id": client_id,
            "client_secret": client_secret,
        }
        if self.audience:
            payload["audience"] = self.audience
        return payload


@dataclass
class RefreshTokenRequest:
    refresh_token: str
    scope: Optional[str] = None

    def to_token_payload(self, client_id: str, client_secret: str) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "client_id": client_id,
            "client_secret": client_secret,
        }
        if self.scope:
            payload["scope"] = self.scope
        return payload


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
class AuthTokens:
    access_token: str
    token_type: str
    expires_in: int
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    scope: Optional[str] = None

    @classmethod
    def from_auth0(cls, payload: Dict[str, Any]) -> "AuthTokens":
        return cls(
            access_token=payload["access_token"],
            token_type=payload.get("token_type", "Bearer"),
            expires_in=int(payload.get("expires_in", 0)),
            id_token=payload.get("id_token"),
            refresh_token=payload.get("refresh_token"),
            scope=payload.get("scope"),
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class UserRecord:
    user_id: str
    email: str
    email_verified: bool
    name: Optional[str] = None
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    created_at: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_auth0(cls, payload: Dict[str, Any]) -> "UserRecord":
        return cls(
            user_id=payload["user_id"],
            email=payload["email"],
            email_verified=bool(payload.get("email_verified", False)),
            name=payload.get("name"),
            given_name=payload.get("given_name"),
            family_name=payload.get("family_name"),
            created_at=payload.get("created_at"),
            raw=payload,
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class TranslationResult:
    translated_text: str
    detected_source_language: Optional[str] = None
    target_language: Optional[str] = None


@dataclass
class ModerationResult:
    allowed: bool
    flagged_categories: List[str]
    scores: Dict[str, float]
    provider: str = "Perspective API"


@dataclass
class OnboardingSummary:
    summary: str
    model: str
    provider: str


@dataclass
class StoredProfileNote:
    note_id: str
    status: str
    document: Dict[str, Any]
