from dataclasses import dataclass
from typing import Optional

@dataclass
class UserRegistration:
    email: str
    password: str

@dataclass
class UserLogin:
    email: str
    password: str

@dataclass
class AuthTokens:
    id_token: str
    refresh_token: str
    expires_in: int
    local_id: str

@dataclass
class PasswordResetRequest:
    email: str

@dataclass
class UserProfile:
    user_id: str
    profile_text: str
    locale: str

@dataclass
class OnboardingNote:
    user_id: str
    timestamp: str
    note_content: str
    support_metadata: dict
