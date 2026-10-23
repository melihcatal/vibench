"""
Local request, response, and normalization helpers for Email/Password Account Lifecycle.

Defines dataclasses for user registration, login, session management,
and password reset flows using Auth0-style response structures.
"""

from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, Any, List
from datetime import datetime


@dataclass
class RegisterUserRequest:
    """Normalized request payload for user registration."""
    email: str
    password: str
    connection: str = "Username-Password-Authentication"
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    def to_auth0_payload(self) -> Dict[str, Any]:
        """Convert to Auth0 Create User payload format."""
        payload: Dict[str, Any] = {
            "email": self.email,
            "password": self.password,
            "connection": self.connection,
        }
        if self.given_name or self.family_name:
            payload["user_metadata"] = {}
            if self.given_name:
                payload["user_metadata"]["given_name"] = self.given_name
            if self.family_name:
                payload["user_metadata"]["family_name"] = self.family_name
        if self.metadata:
            payload.setdefault("user_metadata", {}).update(self.metadata)
        return payload


@dataclass
class RegisteredUserResponse:
    """Normalized response from user registration."""
    user_id: str
    email: str
    email_verified: bool
    created_at: Optional[str] = None
    username: Optional[str] = None

    @classmethod
    def from_auth0_response(cls, data: Dict[str, Any]) -> "RegisteredUserResponse":
        return cls(
            user_id=data.get("user_id", ""),
            email=data.get("email", ""),
            email_verified=data.get("email_verified", False),
            created_at=data.get("created_at"),
            username=data.get("username"),
        )


@dataclass
class LoginRequest:
    """Normalized request for email/password login."""
    email: str
    password: str
    audience: Optional[str] = None
    scope: str = "openid profile email"
    grant_type: str = "http://auth0.com/oauth/grant-type/password-realm"
    realm: str = "Username-Password-Authentication"

    def to_auth0_payload(self) -> Dict[str, Any]:
        """Convert to Auth0 OAuth2 token endpoint payload."""
        payload: Dict[str, Any] = {
            "grant_type": self.grant_type,
            "username": self.email,
            "password": self.password,
            "realm": self.realm,
            "scope": self.scope,
        }
        if self.audience:
            payload["audience"] = self.audience
        return payload


@dataclass
class LoginResponse:
    """Normalized response from successful login."""
    access_token: str
    id_token: str
    token_type: str = "Bearer"
    expires_in: int = 86400
    scope: Optional[str] = None
    refresh_token: Optional[str] = None

    @classmethod
    def from_auth0_response(cls, data: Dict[str, Any]) -> "LoginResponse":
        return cls(
            access_token=data.get("access_token", ""),
            id_token=data.get("id_token", ""),
            token_type=data.get("token_type", "Bearer"),
            expires_in=data.get("expires_in", 86400),
            scope=data.get("scope"),
            refresh_token=data.get("refresh_token"),
        )


@dataclass
class RefreshRequest:
    """Normalized request for token refresh."""
    refresh_token: str
    grant_type: str = "refresh_token"
    client_id: Optional[str] = None

    def to_auth0_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "grant_type": self.grant_type,
            "refresh_token": self.refresh_token,
        }
        if self.client_id:
            payload["client_id"] = self.client_id
        return payload


@dataclass
class RefreshResponse:
    """Normalized response from token refresh."""
    access_token: str
    id_token: Optional[str] = None
    token_type: str = "Bearer"
    expires_in: int = 86400
    scope: Optional[str] = None
    refresh_token: Optional[str] = None

    @classmethod
    def from_auth0_response(cls, data: Dict[str, Any]) -> "RefreshResponse":
        return cls(
            access_token=data.get("access_token", ""),
            id_token=data.get("id_token"),
            token_type=data.get("token_type", "Bearer"),
            expires_in=data.get("expires_in", 86400),
            scope=data.get("scope"),
            refresh_token=data.get("refresh_token"),
        )


@dataclass
class PasswordResetRequest:
    """Normalized request to initiate a password reset."""
    email: str
    connection: str = "Username-Password-Authentication"
    client_id: Optional[str] = None

    def to_auth0_payload(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "email": self.email,
            "connection": self.connection,
        }
        if self.client_id:
            payload["client_id"] = self.client_id
        return payload


@dataclass
class PasswordResetResponse:
    """Normalized response from password reset initiation."""
    email: str
    message: Optional[str] = None
    ticket_url: Optional[str] = None
    success: bool = True


@dataclass
class IdentityError:
    """Standardized identity error representation."""
    error_code: str
    error_description: str
    status_code: int = 400
    details: Optional[Dict[str, Any]] = None

    @classmethod
    def from_auth0_error(cls, data: Dict[str, Any], status_code: int = 400) -> "IdentityError":
        return cls(
            error_code=data.get("error", "unknown_error"),
            error_description=data.get("error_description", data.get("message", "Unknown error")),
            status_code=status_code,
            details=data,
        )
