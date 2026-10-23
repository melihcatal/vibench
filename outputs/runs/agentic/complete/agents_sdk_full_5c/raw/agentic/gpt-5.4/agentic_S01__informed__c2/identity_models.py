from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass(slots=True)
class UserRegistration:
    email: str
    password: str
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    name: Optional[str] = None
    user_metadata: Dict[str, Any] = field(default_factory=dict)
    app_metadata: Dict[str, Any] = field(default_factory=dict)
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
        if self.name:
            payload["name"] = self.name
        if self.user_metadata:
            payload["user_metadata"] = self.user_metadata
        if self.app_metadata:
            payload["app_metadata"] = self.app_metadata
        return payload


@dataclass(slots=True)
class LoginRequest:
    email: str
    password: str
    audience: Optional[str] = None
    scope: str = "openid profile email offline_access"
    realm: str = "Username-Password-Authentication"

    def to_auth0_password_payload(self, client_id: str, client_secret: Optional[str] = None) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "grant_type": "http://auth0.com/oauth/grant-type/password-realm",
            "username": self.email,
            "password": self.password,
            "realm": self.realm,
            "scope": self.scope,
            "client_id": client_id,
        }
        if client_secret:
            payload["client_secret"] = client_secret
        if self.audience:
            payload["audience"] = self.audience
        return payload


@dataclass(slots=True)
class TokenRefreshRequest:
    refresh_token: str
    scope: Optional[str] = None

    def to_auth0_payload(self, client_id: str, client_secret: Optional[str] = None) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "client_id": client_id,
        }
        if client_secret:
            payload["client_secret"] = client_secret
        if self.scope:
            payload["scope"] = self.scope
        return payload


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
class TokenSet:
    access_token: str
    token_type: str
    expires_in: Optional[int] = None
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None
    scope: Optional[str] = None

    @classmethod
    def from_auth0(cls, data: Dict[str, Any]) -> "TokenSet":
        return cls(
            access_token=data["access_token"],
            token_type=data.get("token_type", "Bearer"),
            expires_in=data.get("expires_in"),
            refresh_token=data.get("refresh_token"),
            id_token=data.get("id_token"),
            scope=data.get("scope"),
        )


@dataclass(slots=True)
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
    def from_auth0(cls, data: Dict[str, Any]) -> "UserRecord":
        return cls(
            user_id=data["user_id"],
            email=data["email"],
            email_verified=bool(data.get("email_verified", False)),
            name=data.get("name"),
            given_name=data.get("given_name"),
            family_name=data.get("family_name"),
            created_at=data.get("created_at"),
            raw=data,
        )


def normalize_profile_text(text: str) -> str:
    return " ".join(text.split())


def normalize_locale(locale: str) -> str:
    return locale.replace("_", "-").strip() or "en"
