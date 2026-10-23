from dataclasses import dataclass

@dataclass
class RegisterUserRequest:
    email: str
    password: str = None

@dataclass
class RegisterUserResponse:
    user_id: str
    message: str

@dataclass
class LoginRequest:
    email: str
    password: str

@dataclass
class LoginResponse:
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str

@dataclass
class RefreshSessionRequest:
    refresh_token: str

@dataclass
class RefreshSessionResponse:
    access_token: str
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
    source_language: str = "en"

@dataclass
class TranslateResponse:
    translated_text: str

@dataclass
class ModerationRequest:
    text: str

@dataclass
class ModerationResponse:
    is_moderated: bool
    moderation_details: dict

@dataclass
class SummarizeRequest:
    text: str

@dataclass
class SummarizeResponse:
    summary: str

@dataclass
class ProfileNote:
    user_id: str
    note_content: str
    timestamp: str
    metadata: dict

@dataclass
class StoreNoteResponse:
    note_id: str
    message: str
