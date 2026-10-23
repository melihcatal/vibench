from typing import Dict, Any, Optional
from pydantic import BaseModel, EmailStr


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    username: Optional[str] = None


class RegisterResponse(BaseModel):
    user_id: str
    email: EmailStr
    status: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str


class RefreshRequest(BaseModel):
    refresh_token: str


class RefreshResponse(BaseModel):
    access_token: str
    expires_in: int
    token_type: str


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetResponse(BaseModel):
    status: str
    message: str


def normalize_register_response(data: Dict[str, Any]) -> RegisterResponse:
    return RegisterResponse(
        user_id=data.get("id", ""),
        email=data.get("email", ""),
        status=data.get("status", "active"),
    )


def normalize_login_response(data: Dict[str, Any]) -> LoginResponse:
    return LoginResponse(
        access_token=data.get("access_token", ""),
        refresh_token=data.get("refresh_token", ""),
        expires_in=data.get("expires_in", 3600),
        token_type=data.get("token_type", "Bearer"),
    )


def normalize_refresh_response(data: Dict[str, Any]) -> RefreshResponse:
    return RefreshResponse(
        access_token=data.get("access_token", ""),
        expires_in=data.get("expires_in", 3600),
        token_type=data.get("token_type", "Bearer"),
    )


def normalize_password_reset_response(data: Dict[str, Any]) -> PasswordResetResponse:
    return PasswordResetResponse(
        status=data.get("status", "success"),
        message=data.get("message", "Password reset email sent"),
    )
