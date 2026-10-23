from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def compact_dict(values: Dict[str, Any]) -> Dict[str, Any]:
    return {key: value for key, value in values.items() if value is not None}


@dataclass
class RegisterUserRequest:
    email: str
    password: str
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    connection: str = "Username-Password-Authentication"
    user_metadata: Dict[str, Any] = field(default_factory=dict)

    def to_auth0_payload(self) -> Dict[str, Any]:
        return compact_dict(
            {
                "email": self.email,
                "password": self.password,
                "connection": self.connection,
                "given_name": self.given_name,
                "family_name": self.family_name,
                "user_metadata": self.user_metadata or None,
            }
        )


@dataclass
class LoginRequest:
    email: str
    password: str
    audience: Optional[str] = None
    scope: str = "openid profile email offline_access"
    realm: str = "Username-Password-Authentication"

    def to_auth0_payload(
        self, client_id: str, client_secret: Optional[str]
    ) -> Dict[str, Any]:
        return compact_dict(
            {
                "grant_type": "http://auth0.com/oauth/grant-type/password-realm",
                "username": self.email,
                "password": self.password,
                "realm": self.realm,
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

    def to_auth0_payload(
        self, client_id: str, client_secret: Optional[str]
    ) -> Dict[str, Any]:
        return compact_dict(
            {
                "grant_type": "refresh_token",
                "refresh_token": self.refresh_token,
                "scope": self.scope,
                "client_id": client_id,
                "client_secret": client_secret,
            }
        )


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
class TokenResponse:
    access_token: str
    expires_in: int
    token_type: str
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    scope: Optional[str] = None


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


@dataclass
class TranslationResult:
    translated_text: str
    source_language: Optional[str]
    target_language: str
    provider: str = "deepl"


@dataclass
class ModerationResult:
    approved: bool
    provider: str
    scores: Dict[str, float]
    flagged_categories: List[str]
    raw_response: Dict[str, Any]


@dataclass
class OnboardingSummary:
    user_id: str
    summary: str
    provider: str
    model: str


@dataclass
class ProfileNoteRecord:
    note_id: str
    user_id: str
    status: str
    locale: Optional[str] = None
    notes: Optional[str] = None
    support_metadata: Dict[str, Any] = field(default_factory=dict)


def normalize_auth0_user(payload: Dict[str, Any]) -> UserAccount:
    return UserAccount(
        user_id=payload["user_id"],
        email=payload["email"],
        email_verified=bool(payload.get("email_verified", False)),
        created_at=payload.get("created_at"),
        name=payload.get("name"),
        given_name=payload.get("given_name"),
        family_name=payload.get("family_name"),
        user_metadata=payload.get("user_metadata") or {},
    )


def normalize_token_response(payload: Dict[str, Any]) -> TokenResponse:
    return TokenResponse(
        access_token=payload["access_token"],
        expires_in=int(payload["expires_in"]),
        token_type=payload.get("token_type", "Bearer"),
        id_token=payload.get("id_token"),
        refresh_token=payload.get("refresh_token"),
        scope=payload.get("scope"),
    )
