from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import datetime


@dataclass
class UserRegistrationRequest:
    email: str
    password: str
    display_name: Optional[str] = None
    phone_number: Optional[str] = None
    photo_url: Optional[str] = None

    def to_firebase_dict(self) -> Dict[str, Any]:
        """Convert to Firebase create user payload."""
        data = {
            "email": self.email,
            "password": self.password,
        }
        if self.display_name:
            data["display_name"] = self.display_name
        if self.phone_number:
            data["phone_number"] = self.phone_number
        if self.photo_url:
            data["photo_url"] = self.photo_url
        return data


@dataclass
class UserLoginRequest:
    email: str
    password: str
    return_secure_token: bool = True

    def to_firebase_dict(self) -> Dict[str, Any]:
        """Convert to Firebase login payload."""
        return {
            "email": self.email,
            "password": self.password,
            "returnSecureToken": self.return_secure_token,
        }


@dataclass
class TokenRefreshRequest:
    refresh_token: str
    grant_type: str = "refresh_token"

    def to_firebase_dict(self) -> Dict[str, Any]:
        """Convert to Firebase token refresh payload."""
        return {"grant_type": self.grant_type, "refresh_token": self.refresh_token}


@dataclass
class PasswordResetRequest:
    email: str
    request_type: str = "PASSWORD_RESET"

    def to_firebase_dict(self) -> Dict[str, Any]:
        """Convert to Firebase password reset payload."""
        return {"requestType": self.request_type, "email": self.email}


@dataclass
class UserResponse:
    id: str
    email: str
    display_name: Optional[str]
    email_verified: bool
    created_at: Optional[datetime]
    provider: str = "firebase"

    @classmethod
    def from_firebase_user(cls, user_record) -> "UserResponse":
        """Create from Firebase UserRecord."""
        return cls(
            id=user_record.uid,
            email=user_record.email,
            display_name=user_record.display_name,
            email_verified=user_record.email_verified,
            created_at=user_record.user_metadata.creation_timestamp,
            provider="firebase",
        )

    @classmethod
    def from_firebase_response(cls, data: Dict[str, Any]) -> "UserResponse":
        """Create from Firebase REST API response."""
        return cls(
            id=data.get("localId") or data.get("uid"),
            email=data.get("email"),
            display_name=data.get("displayName"),
            email_verified=data.get("emailVerified", False),
            created_at=datetime.fromtimestamp(int(data.get("createdAt", "0")) / 1000)
            if data.get("createdAt")
            else None,
            provider="firebase",
        )


@dataclass
class TokenResponse:
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str = "Bearer"
    user_id: Optional[str] = None
    provider: str = "firebase"

    @classmethod
    def from_firebase_response(cls, data: Dict[str, Any]) -> "TokenResponse":
        """Create from Firebase REST API response."""
        return cls(
            access_token=data.get("idToken") or data.get("id_token"),
            refresh_token=data.get("refreshToken") or data.get("refresh_token"),
            expires_in=int(data.get("expiresIn") or data.get("expires_in") or 3600),
            token_type=data.get("token_type", "Bearer"),
            user_id=data.get("localId") or data.get("user_id"),
            provider="firebase",
        )


@dataclass
class PasswordResetResponse:
    email: str
    request_type: str
    success: bool
    message: str
    provider: str = "firebase"

    @classmethod
    def from_firebase_response(cls, data: Dict[str, Any]) -> "PasswordResetResponse":
        """Create from Firebase REST API response."""
        return cls(
            email=data.get("email", ""),
            request_type="PASSWORD_RESET",
            success=True,
            message="Password reset email sent successfully",
            provider="firebase",
        )


@dataclass
class ErrorResponse:
    code: str
    message: str
    details: Optional[Dict[str, Any]] = None

    @classmethod
    def from_firebase_error(cls, error_message: str) -> "ErrorResponse":
        """Create from Firebase error message."""
        error_map = {
            "EMAIL_NOT_FOUND": "No user found with this email address",
            "INVALID_PASSWORD": "Invalid password",
            "USER_DISABLED": "User account is disabled",
            "EMAIL_EXISTS": "Email already exists",
            "OPERATION_NOT_ALLOWED": "Password sign-in is disabled",
            "TOO_MANY_ATTEMPTS_TRY_LATER": "Too many attempts. Please try again later.",
            "INVALID_REFRESH_TOKEN": "Invalid or expired refresh token",
            "TOKEN_EXPIRED": "Token has expired",
        }

        message = error_map.get(error_message, "Authentication failed")
        return cls(
            code=error_message, message=message, details={"provider": "firebase"}
        )
