import dataclasses
from typing import Optional


@dataclasses.dataclass
class UserRegistrationRequest:
    email: str
    password: str
    connection: str = "Username-Password-Authentication"


@dataclasses.dataclass
class UserLoginRequest:
    email: str
    password: str
    realm: str = "Username-Password-Authentication"
    scope: str = "openid profile email offline_access"
    audience: Optional[str] = None


@dataclasses.dataclass
class TokenRefreshRequest:
    refresh_token: str


@dataclasses.dataclass
class PasswordResetRequest:
    email: str
    connection: str = "Username-Password-Authentication"


@dataclasses.dataclass
class AuthResponse:
    access_token: str
    expires_in: int
    token_type: str
    refresh_token: Optional[str] = None
    id_token: Optional[str] = None


@dataclasses.dataclass
class UserProfile:
    user_id: str
    email: str
    email_verified: bool
    created_at: str
    updated_at: str
    name: Optional[str] = None
    picture: Optional[str] = None
