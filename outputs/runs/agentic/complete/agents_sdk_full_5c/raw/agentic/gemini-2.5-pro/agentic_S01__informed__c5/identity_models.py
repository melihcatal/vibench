from dataclasses import dataclass
from typing import Optional, Dict

@dataclass
class NewUser:
    email: str
    password: str
    attributes: Optional[Dict[str, str]] = None

@dataclass
class UserLogin:
    email: str
    password: str

@dataclass
class RefreshRequest:
    refresh_token: str

@dataclass
class PasswordResetRequest:
    email: str

@dataclass
class AuthTokens:
    access_token: str
    id_token: str
    refresh_token: Optional[str] = None
    
@dataclass
class UserRegistration:
    user_id: str
    confirmed: bool

@dataclass
class ModerationResult:
    is_safe: bool
    details: Optional[Dict] = None

@dataclass
class OnboardingNote:
    user_id: str
    note_id: str
    content: str
    timestamp: str
