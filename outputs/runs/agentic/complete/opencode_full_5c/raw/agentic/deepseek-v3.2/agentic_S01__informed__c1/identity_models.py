from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class UserRegistrationRequest:
    email: str
    password: str
    user_attributes: Optional[Dict[str, str]] = None


@dataclass
class UserRegistrationResponse:
    success: bool
    user_id: Optional[str]
    email: str
    message: str
    requires_confirmation: bool


@dataclass
class LoginRequest:
    email: str
    password: str


@dataclass
class LoginResponse:
    success: bool
    access_token: Optional[str]
    refresh_token: Optional[str]
    id_token: Optional[str]
    expires_in: Optional[int]
    token_type: Optional[str]
    message: str


@dataclass
class RefreshRequest:
    refresh_token: str


@dataclass
class RefreshResponse:
    success: bool
    access_token: Optional[str]
    id_token: Optional[str]
    expires_in: Optional[int]
    token_type: Optional[str]
    message: str


@dataclass
class PasswordResetRequest:
    email: str


@dataclass
class PasswordResetResponse:
    success: bool
    email: str
    delivery_medium: Optional[str]
    destination: Optional[str]
    message: str


@dataclass
class UserProfile:
    user_id: str
    email: str
    email_verified: bool
    created_at: str
    last_login: Optional[str]
    attributes: Dict[str, str]


def normalize_user_attributes(attributes: Dict[str, Any]) -> Dict[str, str]:
    """Normalize user attributes to string values."""
    normalized = {}
    for key, value in attributes.items():
        if value is None:
            normalized[key] = ""
        else:
            normalized[key] = str(value)
    return normalized


def parse_cognito_attributes(cognito_attributes: list) -> Dict[str, str]:
    """Parse Cognito user attributes list to dictionary."""
    result = {}
    for attr in cognito_attributes:
        name = attr.get("Name", "")
        value = attr.get("Value", "")
        if name:
            result[name] = value
    return result
