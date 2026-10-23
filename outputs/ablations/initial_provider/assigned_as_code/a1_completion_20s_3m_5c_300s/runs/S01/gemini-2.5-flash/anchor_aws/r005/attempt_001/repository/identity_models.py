from dataclasses import dataclass, field
from typing import Optional, Dict


@dataclass
class AuthChallengeResponse:
    challenge_name: str
    session: str
    challenge_parameters: Dict

@dataclass
class AuthResponse:
    access_token: Optional[str] = None
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None
    token_type: Optional[str] = None
    challenge: Optional[AuthChallengeResponse] = None
    user_confirmed: bool = False
    new_password_required: bool = False

@dataclass
class UserRegistrationRequest:
    email: str
    password: str

@dataclass
class UserLoginRequest:
    email: str
    password: str

@dataclass
class PasswordResetRequest:
    email: str

@dataclass
class RefreshSessionRequest:
    refresh_token: str
