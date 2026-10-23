import os
from dataclasses import dataclass, field, asdict
from typing import Optional, List, Dict, Any


@dataclass
class RegisterUserRequest:
    email: str
    password: str
    connection: str = "Username-Password-Authentication"
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class LoginRequest:
    email: str
    password: str
    connection: str = "Username-Password-Authentication"
    audience: Optional[str] = None
    scope: str = "openid profile email"


@dataclass
class RefreshRequest:
    refresh_token: str
    client_id: str
    audience: Optional[str] = None


@dataclass
class PasswordResetRequest:
    email: str
    connection: str = "Username-Password-Authentication"


@dataclass
class AuthResponse:
    access_token: Optional[str] = None
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    token_type: str = "Bearer"
    expires_in: int = 0
    scope: str = ""
    user_id: Optional[str] = None
    email: Optional[str] = None
    email_verified: bool = False
    raw_response: Optional[Dict[str, Any]] = field(default_factory=dict)


@dataclass
class PasswordResetResponse:
    email: str
    status: str = "initiated"
    message: Optional[str] = None


def normalize_register_payload(req: RegisterUserRequest) -> Dict[str, Any]:
    payload = {
        "email": req.email,
        "password": req.password,
        "connection": req.connection,
    }
    if req.given_name:
        payload["given_name"] = req.given_name
    if req.family_name:
        payload["family_name"] = req.family_name
    if req.metadata:
        payload["user_metadata"] = req.metadata
    return payload


def normalize_login_payload(
    req: LoginRequest, client_id: str, client_secret: str
) -> Dict[str, Any]:
    payload = {
        "grant_type": "password",
        "username": req.email,
        "password": req.password,
        "client_id": client_id,
        "client_secret": client_secret,
        "audience": req.audience or "",
        "scope": req.scope,
    }
    return payload


def normalize_refresh_payload(
    req: RefreshRequest, client_secret: str
) -> Dict[str, Any]:
    payload = {
        "grant_type": "refresh_token",
        "client_id": req.client_id,
        "client_secret": client_secret,
        "refresh_token": req.refresh_token,
    }
    if req.audience:
        payload["audience"] = req.audience
    return payload


def normalize_password_reset_payload(
    req: PasswordResetRequest, client_id: str
) -> Dict[str, Any]:
    return {
        "email": req.email,
        "connection": req.connection,
        "client_id": client_id,
    }


def parse_auth_response(data: Dict[str, Any]) -> AuthResponse:
    return AuthResponse(
        access_token=data.get("access_token"),
        id_token=data.get("id_token"),
        refresh_token=data.get("refresh_token"),
        token_type=data.get("token_type", "Bearer"),
        expires_in=int(data.get("expires_in", 0)),
        scope=data.get("scope", ""),
        user_id=data.get("user_id"),
        email=data.get("email"),
        email_verified=data.get("email_verified", False),
        raw_response=data,
    )


def parse_password_reset_response(
    data: Dict[str, Any], email: str
) -> PasswordResetResponse:
    return PasswordResetResponse(
        email=email,
        status=data.get("status", "initiated"),
        message=data.get("message"),
    )
