from dataclasses import dataclass, asdict
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
class TokenRefreshRequest:
    refresh_token: str # For client-side SDKs, but here we'll use ID token for verification

@dataclass
class PasswordResetRequest:
    email: str

@dataclass
class UserResponse:
    uid: str
    email: str
    message: str

@dataclass
class LoginResponse:
    uid: str
    custom_token: str
    message: str
    id_token: Optional[str] = None # In a real client flow, custom_token exchanges for ID token

@dataclass
class ErrorResponse:
    error: str

@dataclass
class ProfileText:
    text: str
    language_code: Optional[str] = None

@dataclass
class OnboardingSummaryInput:
    user_id: str
    profile_text: str
    onboarding_steps_completed: list[str]

@dataclass
class OnboardingNote:
    user_id: str
    note_type: str
    content: dict
    timestamp: str = ""
