import os
from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, Any, List
from datetime import datetime


@dataclass
class RegisterUserRequest:
    email: str
    password: str
    given_name: str = ""
    family_name: str = ""
    locale: str = "en"
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_auth0_payload(self) -> Dict[str, Any]:
        payload = {
            "email": self.email,
            "password": self.password,
            "connection": "Username-Password-Authentication",
        }
        if self.given_name:
            payload["given_name"] = self.given_name
        if self.family_name:
            payload["family_name"] = self.family_name
        if self.metadata:
            payload["user_metadata"] = self.metadata
        return payload


@dataclass
class LoginRequest:
    email: str
    password: str
    audience: str = ""
    scope: str = "openid profile email"

    def to_auth0_payload(self) -> Dict[str, Any]:
        payload = {
            "grant_type": "http://auth0.com/oauth/grant-type/password-realm",
            "username": self.email,
            "password": self.password,
            "realm": "Username-Password-Authentication",
            "scope": self.scope,
        }
        if self.audience:
            payload["audience"] = self.audience
        return payload


@dataclass
class RefreshTokenRequest:
    refresh_token: str
    audience: str = ""
    scope: str = "openid profile email"

    def to_auth0_payload(self) -> Dict[str, Any]:
        payload = {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
            "scope": self.scope,
        }
        if self.audience:
            payload["audience"] = self.audience
        return payload


@dataclass
class PasswordResetRequest:
    email: str
    connection: str = "Username-Password-Authentication"
    client_id: str = ""

    def to_auth0_payload(self) -> Dict[str, Any]:
        payload = {
            "email": self.email,
            "connection": self.connection,
        }
        if self.client_id:
            payload["client_id"] = self.client_id
        return payload


@dataclass
class TokenResponse:
    access_token: str
    token_type: str = "Bearer"
    expires_in: int = 86400
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None
    scope: Optional[str] = None

    @classmethod
    def from_auth0_response(cls, data: Dict[str, Any]) -> "TokenResponse":
        return cls(
            access_token=data.get("access_token", ""),
            token_type=data.get("token_type", "Bearer"),
            expires_in=data.get("expires_in", 86400),
            refresh_token=data.get("refresh_token"),
            id_token=data.get("id_token"),
            scope=data.get("scope"),
        )


@dataclass
class UserResponse:
    user_id: str
    email: str
    email_verified: bool = False
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    locale: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_auth0_response(cls, data: Dict[str, Any]) -> "UserResponse":
        return cls(
            user_id=data.get("user_id", data.get("sub", "")),
            email=data.get("email", ""),
            email_verified=data.get("email_verified", False),
            given_name=data.get("given_name"),
            family_name=data.get("family_name"),
            locale=data.get("locale"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
            metadata=data.get("user_metadata", {}) or {},
        )


@dataclass
class PasswordResetResponse:
    ticket_id: str
    email: str
    created_at: Optional[str] = None

    @classmethod
    def from_auth0_response(
        cls, data: Dict[str, Any], email: str
    ) -> "PasswordResetResponse":
        return cls(
            ticket_id=data.get("ticket_id", data.get("id", "")),
            email=email,
            created_at=data.get("created_at"),
        )


@dataclass
class ModerationResult:
    is_safe: bool
    categories: Dict[str, float] = field(default_factory=dict)
    flagged_text: List[str] = field(default_factory=list)
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class TranslationResult:
    original_text: str
    translated_text: str
    source_language: str = "auto"
    target_language: str = "en"


@dataclass
class OnboardingSummary:
    user_id: str
    status: str
    summary_text: str
    locale: str = "en"
    generated_at: str = ""
    flags: List[str] = field(default_factory=list)


@dataclass
class ProfileNote:
    user_id: str
    note_type: str
    content: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: str = ""
    note_id: Optional[str] = None
