from pydantic import BaseModel
from typing import Optional


class RegisterUserRequest(BaseModel):
    email: str
    password: str
    display_name: Optional[str] = None


class RegisterUserResponse(BaseModel):
    success: bool
    user_id: Optional[str] = None
    email_verified: Optional[bool] = None
    error: Optional[str] = None


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    success: bool
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_in: Optional[str] = None
    error: Optional[str] = None


class RefreshSessionRequest(BaseModel):
    refresh_token: str


class RefreshSessionResponse(BaseModel):
    success: bool
    access_token: Optional[str] = None
    expires_in: Optional[str] = None
    refresh_token: Optional[str] = None
    error: Optional[str] = None


class PasswordResetRequest(BaseModel):
    email: str


class PasswordResetResponse(BaseModel):
    success: bool
    email: Optional[str] = None
    error: Optional[str] = None


class UserProfile(BaseModel):
    user_id: str
    email: str
    display_name: Optional[str] = None
    locale: Optional[str] = None
    onboarding_status: Optional[str] = None
