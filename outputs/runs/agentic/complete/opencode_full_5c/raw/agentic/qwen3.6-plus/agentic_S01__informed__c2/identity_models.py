import os
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List


@dataclass
class RegisterUserRequest:
    email: str
    password: str
    connection: str = "Username-Password-Authentication"
    user_metadata: Optional[Dict[str, Any]] = None
    app_metadata: Optional[Dict[str, Any]] = None


@dataclass
class RegisterUserResponse:
    user_id: str
    email: str
    email_verified: bool
    created_at: str
    connection: str
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LoginRequest:
    email: str
    password: str
    scope: Optional[str] = None


@dataclass
class LoginResponse:
    access_token: str
    id_token: str
    token_type: str
    expires_in: int
    refresh_token: Optional[str] = None
    scope: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RefreshRequest:
    refresh_token: str
    audience: Optional[str] = None
    scope: Optional[str] = None


@dataclass
class RefreshResponse:
    access_token: str
    id_token: str
    token_type: str
    expires_in: int
    scope: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class PasswordResetRequest:
    user_id: Optional[str] = None
    connection_id: Optional[str] = None
    result_url: Optional[str] = None
    ttl_sec: Optional[int] = None
    include_email_in_redirect: Optional[bool] = None
    email: Optional[str] = None


@dataclass
class PasswordResetResponse:
    ticket_id: str
    ticket_url: str
    raw: Dict[str, Any] = field(default_factory=dict)


def normalize_register_request(req: RegisterUserRequest) -> RegisterUserRequest:
    return RegisterUserRequest(
        email=req.email.strip().lower(),
        password=req.password,
        connection=req.connection or "Username-Password-Authentication",
        user_metadata=req.user_metadata,
        app_metadata=req.app_metadata,
    )


def normalize_login_request(req: LoginRequest) -> LoginRequest:
    return LoginRequest(
        email=req.email.strip().lower(),
        password=req.password,
        scope=req.scope,
    )


def normalize_refresh_request(req: RefreshRequest) -> RefreshRequest:
    return RefreshRequest(
        refresh_token=req.refresh_token.strip(),
        audience=req.audience,
        scope=req.scope,
    )


def normalize_password_reset_request(req: PasswordResetRequest) -> PasswordResetRequest:
    return PasswordResetRequest(
        user_id=req.user_id,
        connection_id=req.connection_id,
        result_url=req.result_url,
        ttl_sec=req.ttl_sec,
        include_email_in_redirect=req.include_email_in_redirect,
        email=req.email.strip().lower() if req.email else None,
    )


def parse_register_response(data: Dict[str, Any]) -> RegisterUserResponse:
    return RegisterUserResponse(
        user_id=data.get("user_id", ""),
        email=data.get("email", ""),
        email_verified=data.get("email_verified", False),
        created_at=data.get("created_at", ""),
        connection=data.get("connection", ""),
        raw=data,
    )


def parse_login_response(data: Dict[str, Any]) -> LoginResponse:
    return LoginResponse(
        access_token=data.get("access_token", ""),
        id_token=data.get("id_token", ""),
        token_type=data.get("token_type", "Bearer"),
        expires_in=data.get("expires_in", 0),
        refresh_token=data.get("refresh_token"),
        scope=data.get("scope"),
        raw=data,
    )


def parse_refresh_response(data: Dict[str, Any]) -> RefreshResponse:
    return RefreshResponse(
        access_token=data.get("access_token", ""),
        id_token=data.get("id_token", ""),
        token_type=data.get("token_type", "Bearer"),
        expires_in=data.get("expires_in", 0),
        scope=data.get("scope"),
        raw=data,
    )


def parse_password_reset_response(data: Dict[str, Any]) -> PasswordResetResponse:
    return PasswordResetResponse(
        ticket_id=data.get("ticket", ""),
        ticket_url=data.get("ticket_url", ""),
        raw=data,
    )
