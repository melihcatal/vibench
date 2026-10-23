from typing import Optional, Dict, Any
from dataclasses import dataclass
from datetime import datetime


@dataclass
class UserRegistrationRequest:
    email: str
    password: str
    display_name: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class UserRegistrationResponse:
    user_id: str
    email: str
    id_token: str
    refresh_token: str
    expires_in: int
    display_name: Optional[str] = None


@dataclass
class LoginRequest:
    email: str
    password: str


@dataclass
class LoginResponse:
    user_id: str
    email: str
    id_token: str
    refresh_token: str
    expires_in: int


@dataclass
class RefreshRequest:
    refresh_token: str


@dataclass
class RefreshResponse:
    id_token: str
    refresh_token: str
    expires_in: int
    token_type: str
    user_id: str


@dataclass
class PasswordResetRequest:
    email: str


@dataclass
class PasswordResetResponse:
    email: str
    request_type: str
    success: bool


@dataclass
class UserProfile:
    user_id: str
    email: str
    display_name: Optional[str]
    created_at: datetime
    last_login: Optional[datetime]
    metadata: Dict[str, Any]


def create_user_profile_from_auth(auth_data: Dict[str, Any]) -> UserProfile:
    """
    Create a UserProfile from authentication response data.
    """
    return UserProfile(
        user_id=auth_data.get("user_id", ""),
        email=auth_data.get("email", ""),
        display_name=auth_data.get("display_name"),
        created_at=datetime.now(),
        last_login=datetime.now(),
        metadata={},
    )
