"""
Local request, response, and normalization helpers for Email/Password Account Lifecycle.
"""

from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone


@dataclass
class RegisterUserRequest:
    """Request payload for registering a new email/password user."""
    email: str
    password: str
    display_name: Optional[str] = None
    photo_url: Optional[str] = None
    email_verified: bool = False
    custom_claims: Optional[Dict[str, Any]] = None

    def to_firebase_payload(self) -> Dict[str, Any]:
        """Normalize to Firebase Auth create_user payload."""
        payload: Dict[str, Any] = {
            "email": self.email,
            "password": self.password,
            "email_verified": self.email_verified,
        }
        if self.display_name:
            payload["display_name"] = self.display_name
        if self.photo_url:
            payload["photo_url"] = self.photo_url
        return payload

    def to_web_signup_payload(self) -> Dict[str, Any]:
        """Normalize to Firebase Identity Toolkit web signup payload."""
        return {
            "email": self.email,
            "password": self.password,
            "returnSecureToken": True,
        }


@dataclass
class LoginRequest:
    """Request payload for email/password login."""
    email: str
    password: str
    return_secure_token: bool = True

    def to_firebase_payload(self) -> Dict[str, Any]:
        """Normalize to Firebase Identity Toolkit signInWithPassword payload."""
        return {
            "email": self.email,
            "password": self.password,
            "returnSecureToken": self.return_secure_token,
        }


@dataclass
class PasswordResetRequest:
    """Request payload for initiating a password reset."""
    email: str
    continue_url: Optional[str] = None
    handle_code_in_app: bool = False
    ios_bundle_id: Optional[str] = None
    android_package_name: Optional[str] = None
    android_install_app: bool = False
    android_minimum_version: Optional[str] = None

    def to_firebase_payload(self) -> Dict[str, Any]:
        """Normalize to Firebase oobCode payload."""
        payload: Dict[str, Any] = {
            "email": self.email,
            "requestType": "PASSWORD_RESET",
        }
        if self.continue_url:
            payload["continueUrl"] = self.continue_url
        if self.handle_code_in_app:
            payload["handleCodeInApp"] = True
        if self.ios_bundle_id:
            payload["iOSBundleId"] = self.ios_bundle_id
        if self.android_package_name:
            payload["androidPackageName"] = self.android_package_name
            payload["androidInstallApp"] = self.android_install_app
            if self.android_minimum_version:
                payload["androidMinimumVersion"] = self.android_minimum_version
        return payload


@dataclass
class RefreshTokenRequest:
    """Request payload for refreshing an expired token."""
    refresh_token: str

    def to_firebase_payload(self) -> Dict[str, Any]:
        """Normalize to Firebase token refresh payload."""
        return {
            "grant_type": "refresh_token",
            "refresh_token": self.refresh_token,
        }


@dataclass
class UserResponse:
    """Normalized response after user registration."""
    uid: str
    email: str
    email_verified: bool
    display_name: Optional[str] = None
    photo_url: Optional[str] = None
    created_at: Optional[str] = None
    provider_data: Optional[List[Dict[str, Any]]] = None
    custom_claims: Optional[Dict[str, Any]] = None

    @classmethod
    def from_firebase_user(cls, user_record) -> "UserResponse":
        """Create from a Firebase admin.auth.UserRecord."""
        return cls(
            uid=user_record.uid,
            email=user_record.email or "",
            email_verified=user_record.email_verified,
            display_name=user_record.display_name,
            photo_url=user_record.photo_url,
            created_at=user_record.user_metadata.creation_timestamp,
            provider_data=[
                {"providerId": p.provider_id, "uid": p.uid, "email": p.email}
                for p in user_record.provider_data
            ] if user_record.provider_data else None,
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SessionTokens:
    """Normalized session token response."""
    id_token: str
    refresh_token: str
    expires_in: int
    token_type: str = "Bearer"
    user_id: Optional[str] = None
    email: Optional[str] = None
    is_new_user: bool = False

    @classmethod
    def from_firebase_rest(cls, response_json: Dict[str, Any]) -> "SessionTokens":
        """Create from Firebase Identity Toolkit REST response."""
        return cls(
            id_token=response_json.get("idToken", ""),
            refresh_token=response_json.get("refreshToken", ""),
            expires_in=int(response_json.get("expiresIn", 3600)),
            user_id=response_json.get("localId"),
            email=response_json.get("email"),
            is_new_user=response_json.get("isNewUser", False),
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class PasswordResetResponse:
    """Normalized password reset response."""
    email: str
    oob_code: str
    reset_link: Optional[str] = None

    @classmethod
    def from_firebase_response(cls, response_json: Dict[str, Any]) -> "PasswordResetResponse":
        """Create from Firebase oobCode response."""
        return cls(
            email=response_json.get("email", ""),
            oob_code=response_json.get("oobCode", ""),
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class UserProfile:
    """Normalized user profile for downstream services."""
    uid: str
    email: str
    display_name: Optional[str] = None
    locale: Optional[str] = "en"
    onboarding_completed: bool = False
    created_at: Optional[str] = None

    @classmethod
    def from_user_response(cls, user_resp: UserResponse, locale: Optional[str] = "en") -> "UserProfile":
        return cls(
            uid=user_resp.uid,
            email=user_resp.email,
            display_name=user_resp.display_name,
            locale=locale,
            created_at=user_resp.created_at,
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
