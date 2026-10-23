"""
Define local request, response, and normalization helpers for Email/Password Account Lifecycle.
Contains dataclasses for registration, login, session refresh, password reset,
and response normalization utilities for Auth0 responses.
"""

from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, Any, List


@dataclass
class RegistrationRequest:
    """Represents a request to register a new email/password user."""
    email: str
    password: str
    given_name: str = ""
    family_name: str = ""
    connection: str = "Username-Password-Authentication"
    user_metadata: Dict[str, Any] = field(default_factory=dict)

    def to_auth0_payload(self) -> Dict[str, Any]:
        """Convert to Auth0 /dbconnections/signup payload."""
        payload = {
            "client_id": "",
            "email": self.email,
            "password": self.password,
            "connection": self.connection,
        }
        if self.given_name or self.family_name:
            payload["user_metadata"] = {
                "given_name": self.given_name,
                "family_name": self.family_name,
            }
        if self.user_metadata:
            payload.setdefault("user_metadata", {}).update(self.user_metadata)
        return payload


@dataclass
class RegistrationResponse:
    """Represents the response from a successful registration."""
    user_id: str = ""
    email: str = ""
    email_verified: bool = False
    connection: str = ""
    created_at: str = ""

    @classmethod
    def from_auth0_response(cls, data: Dict[str, Any]) -> "RegistrationResponse":
        return cls(
            user_id=data.get("_id", ""),
            email=data.get("email", ""),
            email_verified=data.get("email_verified", False),
            connection=data.get("connection", ""),
            created_at=data.get("created_at", ""),
        )


@dataclass
class LoginRequest:
    """Represents a request to authenticate with email/password."""
    email: str
    password: str
    audience: str = ""
    scope: str = "openid profile email"
    grant_type: str = "password"
    client_id: str = ""
    connection: str = "Username-Password-Authentication"

    def to_auth0_payload(self) -> Dict[str, Any]:
        """Convert to Auth0 /oauth/token payload for resource owner password flow."""
        return {
            "grant_type": self.grant_type,
            "username": self.email,
            "password": self.password,
            "audience": self.audience,
            "scope": self.scope,
            "client_id": self.client_id,
            "connection": self.connection,
        }


@dataclass
class TokenResponse:
    """Represents tokens returned after successful authentication."""
    access_token: str = ""
    id_token: str = ""
    refresh_token: str = ""
    token_type: str = "Bearer"
    expires_in: int = 0
    scope: str = ""

    @classmethod
    def from_auth0_response(cls, data: Dict[str, Any]) -> "TokenResponse":
        return cls(
            access_token=data.get("access_token", ""),
            id_token=data.get("id_token", ""),
            refresh_token=data.get("refresh_token", ""),
            token_type=data.get("token_type", "Bearer"),
            expires_in=data.get("expires_in", 0),
            scope=data.get("scope", ""),
        )


@dataclass
class RefreshRequest:
    """Represents a request to refresh an access token."""
    refresh_token: str
    grant_type: str = "refresh_token"
    client_id: str = ""

    def to_auth0_payload(self) -> Dict[str, Any]:
        """Convert to Auth0 /oauth/token refresh payload."""
        return {
            "grant_type": self.grant_type,
            "refresh_token": self.refresh_token,
            "client_id": self.client_id,
        }


@dataclass
class PasswordResetRequest:
    """Represents a request to initiate a password reset."""
    email: str
    connection: str = "Username-Password-Authentication"
    client_id: str = ""

    def to_auth0_payload(self) -> Dict[str, Any]:
        """Convert to Auth0 /dbconnections/change_password payload."""
        return {
            "email": self.email,
            "connection": self.connection,
            "client_id": self.client_id,
        }


@dataclass
class PasswordResetResponse:
    """Represents the response from a password reset initiation."""
    email: str = ""
    connection: str = ""
    reset_status: str = ""

    @classmethod
    def from_auth0_response(cls, data: Dict[str, Any]) -> "PasswordResetResponse":
        return cls(
            email=data.get("email", ""),
            connection=data.get("connection", ""),
            reset_status=data.get("status", "sent"),
        )


def normalize_auth_error(response_data: Dict[str, Any]) -> Dict[str, str]:
    """Normalize Auth0 error responses into a standard format."""
    return {
        "error": response_data.get("error", "unknown_error"),
        "error_description": response_data.get("error_description", response_data.get("description", "")),
        "status_code": str(response_data.get("statusCode", "")),
    }


def extract_user_profile_from_id_token(id_token_claims: Dict[str, Any]) -> Dict[str, Any]:
    """Extract user profile fields from decoded ID token claims."""
    return {
        "user_id": id_token_claims.get("sub", ""),
        "email": id_token_claims.get("email", ""),
        "email_verified": id_token_claims.get("email_verified", False),
        "name": id_token_claims.get("name", ""),
        "given_name": id_token_claims.get("given_name", ""),
        "family_name": id_token_claims.get("family_name", ""),
        "locale": id_token_claims.get("locale", "en"),
        "picture": id_token_claims.get("picture", ""),
        "updated_at": id_token_claims.get("updated_at", ""),
    }
