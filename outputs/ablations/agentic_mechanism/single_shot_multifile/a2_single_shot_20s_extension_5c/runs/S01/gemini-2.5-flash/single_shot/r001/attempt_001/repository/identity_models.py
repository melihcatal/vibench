from pydantic import BaseModel
from typing import Optional

class RegisterUserRequest(BaseModel):
    email: str
    password: str

class RegisterUserResponse(BaseModel):
    uid: str
    email: str
    email_verified: bool

class EmailPasswordLoginRequest(BaseModel):
    email: str
    password: str

class EmailPasswordLoginResponse(BaseModel):
    id_token: str
    refresh_token: str
    expires_in: int
    local_id: str

class RefreshSessionRequest(BaseModel):
    refresh_token: str

class RefreshSessionResponse(BaseModel):
    id_token: str
    refresh_token: str
    expires_in: int
    user_id: str

class PasswordResetRequest(BaseModel):
    email: str

class PasswordResetResponse(BaseModel):
    email: str
    kind: str

class TranslateTextRequest(BaseModel):
    text: str
    target_language_code: str
    source_language_code: Optional[str] = None

class TranslateTextResponse(BaseModel):
    translated_text: str
    detected_language_code: Optional[str] = None

class ModerationRequest(BaseModel):
    text: str

class ModerationResultCategory(BaseModel):
    harassment: bool
    harassment_threatening: bool
    hate: bool
    hate_threatening: bool
    self_harm: bool
    self_harm_intent: bool
    self_harm_instructions: bool
    sexual: bool
    sexual_minors: bool
    violence: bool
    violence_graphic: bool

class ModerationResponse(BaseModel):
    id: str
    flagged: bool
    categories: ModerationResultCategory

class OnboardingSummaryRequest(BaseModel):
    onboarding_steps_completed: list[str]
    user_profile_data: dict
    locale: str

class OnboardingSummaryResponse(BaseModel):
    summary_text: str
    recommendations: list[str]

class ProfileNoteStoreRequest(BaseModel):
    user_id: str
    notes: str
    metadata: dict

class ProfileNoteStoreResponse(BaseModel):
    inserted_id: str