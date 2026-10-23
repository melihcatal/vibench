from typing import TypedDict

class RegisterUserRequest(TypedDict):
    email: str
    password: str

class RegisterUserResponse(TypedDict):
    uid: str
    email: str

class EmailPasswordLoginRequest(TypedDict):
    email: str
    password: str

class EmailPasswordLoginResponse(TypedDict):
    id_token: str
    refresh_token: str
    expires_in: str

class RefreshSessionRequest(TypedDict):
    refresh_token: str

class RefreshSessionResponse(TypedDict):
    id_token: str
    refresh_token: str
    expires_in: str

class PasswordResetRequest(TypedDict):
    email: str

class PasswordResetResponse(TypedDict):
    message: str

class TranslateRequest(TypedDict):
    text: str
    target_language: str

class TranslateResponse(TypedDict):
    translated_text: str

class ModerateProfileRequest(TypedDict):
    text: str

class ModerateProfileResponse(TypedDict):
    is_safe: bool
    reasons: list[str]

class OnboardingSummaryRequest(TypedDict):
    user_id: str
    onboarding_steps_completed: list[str]
    profile_text: str

class OnboardingSummaryResponse(TypedDict):
    summary: str

class ProfileNoteStoreRequest(TypedDict):
    user_id: str
    note_content: str
    metadata: dict

class ProfileNoteStoreResponse(TypedDict):
    document_id: str
