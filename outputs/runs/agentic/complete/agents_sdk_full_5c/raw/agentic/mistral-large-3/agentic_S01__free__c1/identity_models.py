from pydantic import BaseModel
from typing import Optional


class RegisterRequest(BaseModel):
    email: str
    password: str
    locale: str
    profile_text: Optional[str] = None


class RegisterResponse(BaseModel):
    user_id: str
    email: str
    locale: str


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    expires_at: int
    user_id: str


class RefreshSessionRequest(BaseModel):
    refresh_token: str


class RefreshSessionResponse(BaseModel):
    access_token: str
    refresh_token: str
    expires_at: int


class PasswordResetRequest(BaseModel):
    email: str


class PasswordResetResponse(BaseModel):
    success: bool
    message: str


class UserProfile(BaseModel):
    user_id: str
    email: str
    locale: str
    profile_text: Optional[str] = None