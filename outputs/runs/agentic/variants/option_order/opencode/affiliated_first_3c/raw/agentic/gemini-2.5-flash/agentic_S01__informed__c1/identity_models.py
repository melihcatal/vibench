from pydantic import BaseModel, EmailStr, Field
from typing import Optional


# Request and Response models for register_user.py
class RegisterUserRequest(BaseModel):
    email: EmailStr
    password: str = Field(
        min_length=6, description="Password must be at least 6 characters long"
    )
    display_name: Optional[str] = None


class RegisterUserResponse(BaseModel):
    uid: str
    email: EmailStr
    display_name: Optional[str] = None


# Request and Response models for email_password_login.py
class EmailPasswordLoginRequest(BaseModel):
    email: EmailStr
    password: str


class EmailPasswordLoginResponse(BaseModel):
    uid: str
    email: EmailStr
    id_token: str
    refresh_token: str


# Request and Response models for refresh_session.py
class RefreshSessionRequest(BaseModel):
    uid: str  # Firebase Admin SDK needs UID to generate custom tokens
    refresh_token: str  # Though not directly used by Admin SDK, kept for consistency


class RefreshSessionResponse(BaseModel):
    uid: str
    new_id_token: str
    new_refresh_token: str


# Request and Response models for password_reset.py
class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetResponse(BaseModel):
    email: EmailStr
    reset_link: str
