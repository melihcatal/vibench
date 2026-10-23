from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class RegisterUserRequest:
    email: str
    password: str
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    connection: str = "Username-Password-Authentication"

    def to_auth0_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "email": self.email,
            "password": self.password,
            "connection": self.connection,
        }
        if self.given_name:
            payload["given_name"] = self.given_name
        if self.family_name:
            payload["family_name"] = self.family_name
        return payload


@dataclass
class LoginRequest:
    email: str
    password: str
    audience: Optional[str] = None
    scope: str = "openid profile email offline_access"


@dataclass
class RefreshSessionRequest:
    refresh_token: str
    scope: str = "openid profile email offline_access"


@dataclass
class PasswordResetRequest:
    email: str
    connection: str = "Username-Password-Authentication"

    def to_auth0_payload(self, client_id: str) -> Dict[str, Any]:
        return {
            "client_id": client_id,
            "email": self.email,
            "connection": self.connection,
        }


@dataclass
class TokenSet:
    access_token: str
    expires_in: int
    token_type: str
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None
    scope: Optional[str] = None

    @classmethod
    def from_auth0_token_response(cls, data: Dict[str, Any]) -> "TokenSet":
        return cls(
            access_token=data["access_token"],
            expires_in=int(data.get("expires_in", 0)),
            token_type=data.get("token_type", "Bearer"),
            refresh_token=data.get("refresh_token"),
            id_token=data.get("id_token"),
            scope=data.get("scope"),
        )


@dataclass
class IdentityUser:
    user_id: str
    email: str
    email_verified: bool
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    name: Optional[str] = None
    nickname: Optional[str] = None
    picture: Optional[str] = None
    app_metadata: Dict[str, Any] = field(default_factory=dict)
    user_metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_auth0_user(cls, data: Dict[str, Any]) -> "IdentityUser":
        return cls(
            user_id=data["user_id"],
            email=data["email"],
            email_verified=bool(data.get("email_verified", False)),
            given_name=data.get("given_name"),
            family_name=data.get("family_name"),
            name=data.get("name"),
            nickname=data.get("nickname"),
            picture=data.get("picture"),
            app_metadata=data.get("app_metadata") or {},
            user_metadata=data.get("user_metadata") or {},
        )


@dataclass
class TranslationResult:
    locale: str
    translated_text: str
    detected_source_language: Optional[str] = None


@dataclass
class ModerationResult:
    allowed: bool
    category_scores: Dict[str, float]
    flagged_categories: List[str]
    provider: str = "Perspective API"


@dataclass
class OnboardingSummary:
    summary_text: str
    model: str
    provider: str = "OpenAI"


@dataclass
class StoredProfileNote:
    document_id: str
    collection: str
    created: bool
    provider: str = "Cloud Firestore"
