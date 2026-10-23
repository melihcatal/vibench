import os
from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class RegisterRequest:
    email: str
    password: str
    connection: str = "Username-Password-Authentication"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LoginRequest:
    email: str
    password: str
    client_id: str
    client_secret: str
    audience: str
    scope: str = "openid profile email"


@dataclass
class RefreshRequest:
    refresh_token: str
    client_id: str
    audience: Optional[str] = None
    scope: Optional[str] = None


@dataclass
class PasswordResetRequest:
    email: str
    connection: str
    client_id: str


@dataclass
class RegisterResponse:
    user_id: str
    email: str
    email_verified: bool
    created_at: str
    connection: str


@dataclass
class LoginResponse:
    access_token: str
    id_token: str
    token_type: str
    expires_in: int
    scope: str
    refresh_token: Optional[str] = None


@dataclass
class RefreshResponse:
    access_token: str
    id_token: str
    token_type: str
    expires_in: int
    scope: str


@dataclass
class PasswordResetResponse:
    email: str
    connection: str
    status: str


def normalize_register_response(raw: Dict[str, Any]) -> RegisterResponse:
    return RegisterResponse(
        user_id=raw.get("user_id", ""),
        email=raw.get("email", ""),
        email_verified=raw.get("email_verified", False),
        created_at=raw.get("created_at", ""),
        connection=raw.get("connection", ""),
    )


def normalize_login_response(raw: Dict[str, Any]) -> LoginResponse:
    return LoginResponse(
        access_token=raw.get("access_token", ""),
        id_token=raw.get("id_token", ""),
        token_type=raw.get("token_type", "Bearer"),
        expires_in=int(raw.get("expires_in", 0)),
        scope=raw.get("scope", ""),
        refresh_token=raw.get("refresh_token"),
    )


def normalize_refresh_response(raw: Dict[str, Any]) -> RefreshResponse:
    return RefreshResponse(
        access_token=raw.get("access_token", ""),
        id_token=raw.get("id_token", ""),
        token_type=raw.get("token_type", "Bearer"),
        expires_in=int(raw.get("expires_in", 0)),
        scope=raw.get("scope", ""),
    )


def normalize_password_reset_response(raw: Dict[str, Any]) -> PasswordResetResponse:
    return PasswordResetResponse(
        email=raw.get("email", ""),
        connection=raw.get("connection", ""),
        status=raw.get("status", "sent"),
    )
