from dataclasses import dataclass, field
from typing import Optional

@dataclass
class UserRegistrationRequest:
    email: str
    password: str

@dataclass
class UserLoginRequest:
    email: str
    password: str

@dataclass
class AuthTokens:
    id_token: str
    refresh_token: str
    expires_in: int
    token_type: Optional[str] = "Bearer"

@dataclass
class UserProfile:
    uid: str
    email: str
    display_name: Optional[str] = None
    photo_url: Optional[str] = None

@dataclass
class PasswordResetRequest:
    email: str

@dataclass
class OperationResult:
    success: bool
    message: str
    data: Optional[dict] = field(default_factory=dict)

