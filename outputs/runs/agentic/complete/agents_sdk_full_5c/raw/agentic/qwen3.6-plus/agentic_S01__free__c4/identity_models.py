"""
Local request, response, and normalization helpers for Email/Password Account Lifecycle.

Provides Pydantic models for Auth0 request/response payloads and
utility functions for normalizing user data across the identity flow.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict
from typing import Any, Dict, List, Optional


@dataclass
class RegisterRequest:
    """Normalized registration payload for email/password account creation."""
    email: str
    password: str
    connection: str = "Username-Password-Authentication"
    user_metadata: Optional[Dict[str, Any]] = None

    def to_auth0_payload(self) -> Dict[str, Any]:
        """Convert to Auth0 /dbconnections/signup payload format."""
        payload: Dict[str, Any] = {
            "client_id": "",  # filled in by caller from config
            "email": self.email,
            "password": self.password,
            "connection": self.connection,
        }
        if self.user_metadata:
            payload["user_metadata"] = self.user_metadata
        return payload


@dataclass
class LoginRequest:
    """Normalized login payload for email/password authentication."""
    email: str
    password: str
    audience: str = ""
    scope: str = "openid profile email"
    grant_type: str = "password"

    def to_auth0_payload(self, client_id: str) -> Dict[str, Any]:
        """Convert to Auth0 /oauth/token payload format."""
        return {
            "grant_type": self.grant_type,
            "username": self.email,
            "password": self.password,
            "client_id": client_id,
            "audience": self.audience,
            "scope": self.scope,
        }


@dataclass
class LoginResponse:
    """Normalized response from a successful email/password login."""
    access_token: str
    id_token: str
    refresh_token: Optional[str] = None
    token_type: str = "Bearer"
    expires_in: int = 86400
    scope: Optional[str] = None

    @classmethod
    def from_auth0_response(cls, raw: Dict[str, Any]) -> "LoginResponse":
        """Normalize an Auth0 /oauth/token response into a LoginResponse."""
        return cls(
            access_token=raw["access_token"],
            id_token=raw["id_token"],
            refresh_token=raw.get("refresh_token"),
            token_type=raw.get("token_type", "Bearer"),
            expires_in=raw.get("expires_in", 86400),
            scope=raw.get("scope"),
        )


@dataclass
class RefreshRequest:
    """Normalized refresh token request."""
    refresh_token: str
    client_id: str = ""

    def to_auth0_payload(self) -> Dict[str, Any]:
        """Convert to Auth0 /oauth/token refresh payload."""
        return {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "refresh_token": self.refresh_token,
        }


@dataclass
class PasswordResetRequest:
    """Normalized password reset request payload."""
    email: str
    connection: str = "Username-Password-Authentication"
    client_id: str = ""

    def to_auth0_payload(self) -> Dict[str, Any]:
        """Convert to Auth0 /dbconnections/change_password payload."""
        return {
            "client_id": self.client_id,
            "email": self.email,
            "connection": self.connection,
        }


@dataclass
class RegisterResponse:
    """Normalized response from user registration."""
    user_id: str
    email: str
    email_verified: bool = False
    user_metadata: Optional[Dict[str, Any]] = None

    @classmethod
    def from_auth0_response(cls, raw: Dict[str, Any]) -> "RegisterResponse":
        """Normalize an Auth0 signup response."""
        return cls(
            user_id=raw.get("_id", ""),
            email=raw.get("email", ""),
            email_verified=raw.get("email_verified", False),
            user_metadata=raw.get("user_metadata"),
        )


def normalize_user_email(email: str) -> str:
    """Normalize email address for identity operations."""
    return email.strip().lower()


def extract_user_identity(raw_user: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract core identity fields from a raw Auth0 user object.
    Returns a normalized dict with user_id, email, name, and connection.
    """
    return {
        "user_id": raw_user.get("user_id", ""),
        "email": raw_user.get("email", ""),
        "name": raw_user.get("name", ""),
        "email_verified": raw_user.get("email_verified", False),
        "connection": raw_user.get("connection", ""),
        "identities": raw_user.get("identities", []),
    }
