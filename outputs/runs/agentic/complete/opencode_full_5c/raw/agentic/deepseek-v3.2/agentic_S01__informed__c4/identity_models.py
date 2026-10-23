from typing import Optional, Dict, Any, List
from dataclasses import dataclass, asdict
from datetime import datetime
import json


@dataclass
class UserRegistrationRequest:
    """Request model for user registration."""

    email: str
    password: str
    display_name: Optional[str] = None
    email_verified: bool = False

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API calls."""
        data = {
            "email": self.email,
            "password": self.password,
            "email_verified": self.email_verified,
        }
        if self.display_name:
            data["display_name"] = self.display_name
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserRegistrationRequest":
        """Create from dictionary."""
        return cls(
            email=data.get("email", ""),
            password=data.get("password", ""),
            display_name=data.get("display_name"),
            email_verified=data.get("email_verified", False),
        )


@dataclass
class LoginRequest:
    """Request model for user login."""

    email: str
    password: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API calls."""
        return {"email": self.email, "password": self.password}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LoginRequest":
        """Create from dictionary."""
        return cls(email=data.get("email", ""), password=data.get("password", ""))


@dataclass
class TokenRefreshRequest:
    """Request model for token refresh."""

    refresh_token: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API calls."""
        return {"refresh_token": self.refresh_token}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TokenRefreshRequest":
        """Create from dictionary."""
        return cls(refresh_token=data.get("refresh_token", ""))


@dataclass
class PasswordResetRequest:
    """Request model for password reset."""

    email: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API calls."""
        return {"email": self.email}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PasswordResetRequest":
        """Create from dictionary."""
        return cls(email=data.get("email", ""))


@dataclass
class UserResponse:
    """Response model for user operations."""

    user_id: str
    email: str
    display_name: Optional[str]
    email_verified: bool
    created_at: Optional[datetime] = None
    last_login_at: Optional[datetime] = None
    disabled: bool = False
    provider: str = "firebase"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        data = asdict(self)
        # Convert datetime objects to ISO format strings
        if data.get("created_at") and isinstance(data["created_at"], datetime):
            data["created_at"] = data["created_at"].isoformat()
        if data.get("last_login_at") and isinstance(data["last_login_at"], datetime):
            data["last_login_at"] = data["last_login_at"].isoformat()
        return data

    @classmethod
    def from_firebase_user(cls, user_record) -> "UserResponse":
        """Create from Firebase user record."""
        return cls(
            user_id=user_record.uid,
            email=user_record.email,
            display_name=user_record.display_name,
            email_verified=user_record.email_verified,
            created_at=user_record.user_metadata.creation_timestamp,
            last_login_at=user_record.user_metadata.last_sign_in_timestamp,
            disabled=user_record.disabled,
        )


@dataclass
class AuthTokens:
    """Model for authentication tokens."""

    id_token: str
    refresh_token: str
    expires_in: int
    user_id: str
    email: str
    display_name: Optional[str] = None
    provider: str = "firebase"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)

    @classmethod
    def from_firebase_response(cls, data: Dict[str, Any]) -> "AuthTokens":
        """Create from Firebase REST API response."""
        return cls(
            id_token=data.get("idToken", ""),
            refresh_token=data.get("refreshToken", ""),
            expires_in=int(data.get("expiresIn", 3600)),
            user_id=data.get("localId", ""),
            email=data.get("email", ""),
            display_name=data.get("displayName"),
        )


@dataclass
class PasswordResetResponse:
    """Response model for password reset."""

    email: str
    request_type: str
    success: bool
    message: str
    provider: str = "firebase"

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


def normalize_error_response(error: Exception) -> Dict[str, Any]:
    """Normalize error responses for consistent error handling."""
    error_type = type(error).__name__
    error_message = str(error)

    if "Email already exists" in error_message:
        return {
            "error_code": "EMAIL_ALREADY_EXISTS",
            "message": "Email already exists",
            "status": 409,
        }
    elif "Invalid email or password" in error_message:
        return {
            "error_code": "INVALID_CREDENTIALS",
            "message": "Invalid email or password",
            "status": 401,
        }
    elif "Email not found" in error_message:
        return {
            "error_code": "USER_NOT_FOUND",
            "message": "Email not found",
            "status": 404,
        }
    elif "Token has expired" in error_message:
        return {
            "error_code": "TOKEN_EXPIRED",
            "message": "Token has expired",
            "status": 401,
        }
    elif "Invalid or expired refresh token" in error_message:
        return {
            "error_code": "INVALID_REFRESH_TOKEN",
            "message": "Invalid or expired refresh token",
            "status": 401,
        }
    else:
        return {"error_code": "INTERNAL_ERROR", "message": error_message, "status": 500}
