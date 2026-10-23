"""
Local request, response, and normalization helpers for Email/Password Account Lifecycle.
"""

from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, Any, List
from datetime import datetime


@dataclass
class RegistrationRequest:
    """Request model for user registration."""
    email: str
    password: str
    display_name: Optional[str] = None
    locale: Optional[str] = "en-US"

    def to_firebase_payload(self) -> Dict[str, Any]:
        payload = {
            "email": self.email,
            "password": self.password,
            "returnSecureToken": True,
        }
        if self.display_name:
            payload["displayName"] = self.display_name
        return payload


@dataclass
class LoginRequest:
    """Request model for email/password login."""
    email: str
    password: str

    def to_firebase_payload(self) -> Dict[str, Any]:
        return {
            "email": self.email,
            "password": self.password,
            "returnSecureToken": True,
        }


@dataclass
class PasswordResetRequest:
    """Request model for password reset initiation."""
    email: str
    continue_url: Optional[str] = None
    locale: Optional[str] = "en-US"

    def to_firebase_payload(self) -> Dict[str, Any]:
        payload = {
            "requestType": "PASSWORD_RESET",
            "email": self.email,
        }
        if self.continue_url:
            payload["continueUrl"] = self.continue_url
        return payload


@dataclass
class TokenRefreshRequest:
    """Request model for refreshing an access token."""
    refresh_token: str

    def to_firebase_payload(self) -> Dict[str, Any]:
        return {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
        }


@dataclass
class SessionResponse:
    """Normalized session response after auth operations."""
    local_id: Optional[str] = None
    email: Optional[str] = None
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None
    is_new_user: bool = False
    display_name: Optional[str] = None
    created_at: Optional[str] = None

    @classmethod
    def from_firebase_response(cls, response_data: Dict[str, Any]) -> "SessionResponse":
        expires_in = response_data.get("expiresIn")
        try:
            expires_in_seconds = int(expires_in) if expires_in else 3600
        except (ValueError, TypeError):
            expires_in_seconds = 3600

        return cls(
            local_id=response_data.get("localId"),
            email=response_data.get("email"),
            id_token=response_data.get("idToken"),
            refresh_token=response_data.get("refreshToken"),
            expires_in=expires_in_seconds,
            is_new_user=response_data.get("isNewUser", False),
            display_name=response_data.get("displayName"),
            created_at=datetime.utcnow().isoformat() + "Z",
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class PasswordResetResponse:
    """Response model for password reset initiation."""
    email: Optional[str] = None
    request_type: Optional[str] = None
    oob_code: Optional[str] = None

    @classmethod
    def from_firebase_response(cls, response_data: Dict[str, Any]) -> "PasswordResetResponse":
        return cls(
            email=response_data.get("email"),
            request_type=response_data.get("requestType"),
            oob_code=response_data.get("oobCode"),
        )


@dataclass
class AuthError:
    """Standardized auth error representation."""
    code: int
    message: str
    provider_error: Optional[str] = None

    @classmethod
    def from_firebase_error(cls, error_data: Dict[str, Any]) -> "AuthError":
        error_info = error_data.get("error", {})
        return cls(
            code=error_info.get("code", 0),
            message=error_info.get("message", "Unknown error"),
            provider_error=error_info.get("errors", [{}])[0].get("reason"),
        )


def normalize_email(email: str) -> str:
    """Normalize email address for consistent handling."""
    return email.strip().lower()


def mask_email(email: str) -> str:
    """Partially mask email for logging purposes."""
    if "@" not in email:
        return "***"
    local, domain = email.split("@", 1)
    masked_local = local[0] + "***" if local else "***"
    return f"{masked_local}@{domain}"
