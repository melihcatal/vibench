from pydantic import BaseModel
from typing import Optional


class RegisterRequest(BaseModel):
    email: str
    password: str


class RegisterResponse(BaseModel):
    user_id: str
    email: str


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    session_token: str
    session_jwt: str


class RefreshRequest(BaseModel):
    session_token: str


class RefreshResponse(BaseModel):
    session_token: str
    session_jwt: str


class PasswordResetRequest(BaseModel):
    email: str


class PasswordResetStartResponse(BaseModel):
    reset_code_id: str
    expires_at: float
