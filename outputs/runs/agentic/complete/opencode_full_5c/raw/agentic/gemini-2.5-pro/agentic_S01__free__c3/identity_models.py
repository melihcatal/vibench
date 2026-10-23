from pydantic import BaseModel, Field
from typing import Optional


class UserRegistrationRequest(BaseModel):
    email: str
    password: str


class UserRegistrationResponse(BaseModel):
    id_token: str = Field(alias="idToken")
    email: str
    refresh_token: str = Field(alias="refreshToken")
    expires_in: str = Field(alias="expiresIn")
    local_id: str = Field(alias="localId")


class UserLoginRequest(BaseModel):
    email: str
    password: str


class UserLoginResponse(BaseModel):
    id_token: str = Field(alias="idToken")
    email: str
    refresh_token: str = Field(alias="refreshToken")
    expires_in: str = Field(alias="expiresIn")
    local_id: str = Field(alias="localId")
    registered: bool


class RefreshSessionRequest(BaseModel):
    refresh_token: str


class RefreshSessionResponse(BaseModel):
    expires_in: str = Field(alias="expires_in")
    token_type: str = Field(alias="token_type")
    refresh_token: str = Field(alias="refresh_token")
    id_token: str = Field(alias="id_token")
    user_id: str = Field(alias="user_id")
    project_id: str = Field(alias="project_id")


class PasswordResetRequest(BaseModel):
    email: str


class PasswordResetResponse(BaseModel):
    email: str
    kind: str


class TranslationRequest(BaseModel):
    text: str
    target_language: str


class TranslationResponse(BaseModel):
    translated_text: str


class ModerationRequest(BaseModel):
    text: str


class ModerationResponse(BaseModel):
    is_safe: bool
    categories: Optional[dict] = None


class SummaryRequest(BaseModel):
    user_data: dict


class SummaryResponse(BaseModel):
    summary: str


class ProfileNote(BaseModel):
    user_id: str
    note: str


class StoreNoteResponse(BaseModel):
    success: bool
    document_id: Optional[str] = None
