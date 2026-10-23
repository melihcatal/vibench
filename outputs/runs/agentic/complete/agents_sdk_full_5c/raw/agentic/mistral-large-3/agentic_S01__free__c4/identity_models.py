from pydantic import BaseModel
from typing import Optional


class RegisterRequest(BaseModel):
    email: str
    password: str
    name: str


class RegisterResponse(BaseModel):
    user_id: str
    email: str
    created_at: str


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int


class RefreshSessionRequest(BaseModel):
    refresh_token: str


class RefreshSessionResponse(BaseModel):
    access_token: str
    expires_in: int


class PasswordResetRequest(BaseModel):
    email: str


class PasswordResetResponse(BaseModel):
    email_sent: bool
    reset_initiated: bool