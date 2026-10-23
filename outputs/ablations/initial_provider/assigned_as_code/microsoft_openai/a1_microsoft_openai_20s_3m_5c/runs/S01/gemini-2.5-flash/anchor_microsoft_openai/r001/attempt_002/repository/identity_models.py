from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class RegisterUserPayload:
    email: str
    password: str
    tenant_id: Optional[str] = None # For multi-tenant scenarios, if needed

@dataclass
class RegisterUserResponse:
    user_id: str

@dataclass
class LoginPayload:
    email: str
    password: str

@dataclass
class LoginResponse:
    access_token: str
    refresh_token: Optional[str] = None
    expires_in: int
    token_type: str

@dataclass
class RefreshSessionPayload:
    refresh_token: str
    # Or access_token if the flow uses it for refresh

@dataclass
class RefreshSessionResponse:
    access_token: str
    refresh_token: Optional[str] = None
    expires_in: int
    token_type: str

@dataclass
class PasswordResetPayload:
    email: str
    # Add any other fields like redirect_url if the API requires it

@dataclass
class PasswordResetResponse:
    message: str # Or a status/id for the reset request

@dataclass
class WelcomeTranslatePayload:
    text: str
    target_language: str
    source_language: Optional[str] = None

@dataclass
class WelcomeTranslateResponse:
    translated_text: str

@dataclass
class ProfileModerationPayload:
    profile_text: str
    user_id: Optional[str] = None

@dataclass
class ProfileModerationResponse:
    is_moderated: bool
    moderation_details: dict = field(default_factory=dict) # To include details like categories, scores

@dataclass
class OnboardingSummaryPayload:
    user_id: str
    onboarding_data: dict # Any relevant data to summarize

@dataclass
class OnboardingSummaryResponse:
    summary: str

@dataclass
class ProfileNote:
    user_id: str
    note_content: str
    timestamp: str
    author: Optional[str] = None
    category: Optional[str] = None

@dataclass
class ProfileNoteStorePayload:
    note: ProfileNote

@dataclass
class ProfileNoteStoreResponse:
    note_id: str
    status: str
