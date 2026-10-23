import dataclasses

@dataclasses.dataclass
class RegisterUserRequest:
    email: str
    password: str

@dataclasses.dataclass
class RegisterUserResponse:
    user_id: str
    email: str
    message: str

@dataclasses.dataclass
class LoginRequest:
    email: str
    password: str

@dataclasses.dataclass
class LoginResponse:
    access_token: str
    refresh_token: str
    expires_in: int

@dataclasses.dataclass
class RefreshSessionRequest:
    refresh_token: str

@dataclasses.dataclass
class RefreshSessionResponse:
    access_token: str
    expires_in: int

@dataclasses.dataclass
class PasswordResetRequest:
    email: str

@dataclasses.dataclass
class PasswordResetResponse:
    message: str

@dataclasses.dataclass
class TranslateRequest:
    text: str
    target_language: str

@dataclasses.dataclass
class TranslateResponse:
    translated_text: str

@dataclasses.dataclass
class ModerateTextRequest:
    text: str

@dataclasses.dataclass
class ModerateTextResponse:
    flagged: bool
    moderation_details: dict

@dataclasses.dataclass
class OnboardingSummaryRequest:
    user_id: str
    onboarding_steps: list[str]

@dataclasses.dataclass
class OnboardingSummaryResponse:
    summary: str

@dataclasses.dataclass
class ProfileNote:
    user_id: str
    note_content: str
    timestamp: str
    category: str

@dataclasses.dataclass
class StoreProfileNoteRequest:
    note: ProfileNote

@dataclasses.dataclass
class StoreProfileNoteResponse:
    note_id: str
