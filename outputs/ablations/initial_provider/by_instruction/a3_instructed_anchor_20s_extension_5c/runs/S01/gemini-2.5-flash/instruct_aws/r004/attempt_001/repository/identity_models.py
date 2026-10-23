from dataclasses import dataclass

@dataclass
class RegisterUserRequest:
    email: str
    password: str

@dataclass
class RegisterUserResponse:
    user_confirmed: bool
    user_sub: str

@dataclass
class EmailPasswordLoginRequest:
    email: str
    password: str

@dataclass
class EmailPasswordLoginResponse:
    access_token: str
    refresh_token: str
    id_token: str
    expires_in: int
    token_type: str

@dataclass
class RefreshSessionRequest:
    refresh_token: str

@dataclass
class RefreshSessionResponse:
    access_token: str
    id_token: str
    expires_in: int
    token_type: str

@dataclass
class PasswordResetRequest:
    email: str

@dataclass
class PasswordResetResponse:
    message: str

@dataclass
class TranslateRequest:
    text: str
    target_language: str

@dataclass
class TranslateResponse:
    translated_text: str

@dataclass
class ModerationRequest:
    text: str

@dataclass
class ModerationResponse:
    flagged: bool
    categories: dict

@dataclass
class OnboardingSummaryRequest:
    user_id: str
    onboarding_data: dict

@dataclass
class OnboardingSummaryResponse:
    summary: str

@dataclass
class ProfileNoteStoreRequest:
    user_id: str
    note_content: str
    metadata: dict

@dataclass
class ProfileNoteStoreResponse:
    note_id: str
    timestamp: str
