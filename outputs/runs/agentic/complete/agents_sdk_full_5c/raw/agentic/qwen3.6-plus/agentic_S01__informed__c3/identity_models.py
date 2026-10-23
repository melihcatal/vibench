"""
Local request, response, and normalization helpers for Email/Password Account Lifecycle.

Provider context: Auth0 Management API / Authentication API
"""

from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone


@dataclass
class RegisterUserRequest:
    """Normalized request payload for user registration."""
    email: str
    password: str
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    locale: Optional[str] = "en"
    metadata: Optional[Dict[str, Any]] = field(default_factory=dict)

    def to_auth0_payload(self) -> Dict[str, Any]:
        """Convert to Auth0 /api/v2/users creation payload."""
        payload = {
            "email": self.email,
            "password": self.password,
            "connection": "Username-Password-Authentication",
            "email_verified": False,
        }
        if self.given_name or self.family_name:
            payload["name"] = f"{self.given_name or ''} {self.family_name or ''}".strip()
            if self.given_name:
                payload["given_name"] = self.given_name
            if self.family_name:
                payload["family_name"] = self.family_name
        if self.locale:
            payload["app_metadata"] = {"locale": self.locale}
        if self.metadata:
            payload.setdefault("user_metadata", {})
            payload["user_metadata"].update(self.metadata)
        return payload


@dataclass
class LoginRequest:
    """Normalized request payload for email/password login."""
    email: str
    password: str
    audience: Optional[str] = None
    scope: Optional[str] = "openid profile email"

    def to_auth0_payload(self, client_id: str) -> Dict[str, Any]:
        """Convert to Auth0 /oauth/token grant payload."""
        payload = {
            "grant_type": "password",
            "username": self.email,
            "password": self.password,
            "client_id": client_id,
            "scope": self.scope or "openid profile email",
        }
        if self.audience:
            payload["audience"] = self.audience
        return payload


@dataclass
class RefreshTokenRequest:
    """Normalized request payload for token refresh."""
    refresh_token: str

    def to_auth0_payload(self, client_id: str) -> Dict[str, Any]:
        """Convert to Auth0 /oauth/token refresh_token grant payload."""
        return {
            "grant_type": "refresh_token",
            "client_id": client_id,
            "refresh_token": self.refresh_token,
        }


@dataclass
class PasswordResetRequest:
    """Normalized request payload for password reset initiation."""
    email: str
    connection: str = "Username-Password-Authentication"

    def to_auth0_payload(self) -> Dict[str, Any]:
        """Convert to Auth0 /dbconnections/change_password payload."""
        return {
            "client_id": "{client_id}",
            "email": self.email,
            "connection": self.connection,
        }


@dataclass
class Auth0TokenResponse:
    """Normalized response from Auth0 token endpoint."""
    access_token: str
    token_type: str
    expires_in: int
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    scope: Optional[str] = None

    @classmethod
    def from_auth0_response(cls, data: Dict[str, Any]) -> "Auth0TokenResponse":
        """Parse Auth0 /oauth/token response."""
        return cls(
            access_token=data["access_token"],
            token_type=data.get("token_type", "Bearer"),
            expires_in=int(data.get("expires_in", 3600)),
            id_token=data.get("id_token"),
            refresh_token=data.get("refresh_token"),
            scope=data.get("scope"),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "access_token": self.access_token,
            "token_type": self.token_type,
            "expires_in": self.expires_in,
            "id_token": self.id_token,
            "refresh_token": self.refresh_token,
            "scope": self.scope,
        }


@dataclass
class Auth0UserResponse:
    """Normalized response from Auth0 user creation endpoint."""
    user_id: str
    email: str
    email_verified: bool
    created_at: Optional[str] = None
    identities: Optional[List[Dict[str, Any]]] = None
    user_metadata: Optional[Dict[str, Any]] = None

    @classmethod
    def from_auth0_response(cls, data: Dict[str, Any]) -> "Auth0UserResponse":
        """Parse Auth0 /api/v2/users response."""
        created = data.get("created_at")
        if created:
            try:
                dt = datetime.fromisoformat(created.replace("Z", "+00:00"))
                created = dt.isoformat()
            except (ValueError, TypeError):
                pass
        return cls(
            user_id=data.get("user_id", ""),
            email=data.get("email", ""),
            email_verified=data.get("email_verified", False),
            created_at=created,
            identities=data.get("identities"),
            user_metadata=data.get("user_metadata"),
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


def normalize_auth_error(error_data: Dict[str, Any]) -> Dict[str, str]:
    """Normalize Auth0 error responses into a consistent format."""
    return {
        "error": error_data.get("error", "unknown_error"),
        "error_description": error_data.get("error_description", ""),
        "status_code": str(error_data.get("status_code", 0)),
    }
