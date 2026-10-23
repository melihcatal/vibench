from dataclasses import dataclass, field, asdict
from typing import Optional, Any
from datetime import datetime


@dataclass
class RegisterRequest:
    email: str
    password: str
    connection: str = "Username-Password-Authentication"
    client_id: Optional[str] = None
    user_metadata: dict = field(default_factory=dict)
    app_metadata: dict = field(default_factory=dict)

    def to_payload(self) -> dict:
        payload = {
            "email": self.email,
            "password": self.password,
            "connection": self.connection,
        }
        if self.client_id:
            payload["client_id"] = self.client_id
        if self.user_metadata:
            payload["user_metadata"] = self.user_metadata
        if self.app_metadata:
            payload["app_metadata"] = self.app_metadata
        return payload


@dataclass
class RegisterResponse:
    user_id: str
    email: str
    email_verified: bool
    created_at: Optional[str] = None
    raw_response: dict = field(default_factory=dict)

    @classmethod
    def from_auth0_response(cls, data: dict) -> "RegisterResponse":
        return cls(
            user_id=data.get("user_id", data.get("_id", "")),
            email=data.get("email", ""),
            email_verified=data.get("email_verified", False),
            created_at=data.get("created_at"),
            raw_response=data,
        )


@dataclass
class LoginRequest:
    email: str
    password: str
    client_id: Optional[str] = None
    audience: Optional[str] = None
    scope: str = "openid profile email"

    def to_payload(self, client_id: str) -> dict:
        payload = {
            "grant_type": "password",
            "username": self.email,
            "password": self.password,
            "client_id": self.client_id or client_id,
            "scope": self.scope,
        }
        if self.audience:
            payload["audience"] = self.audience
        return payload


@dataclass
class LoginResponse:
    access_token: str
    id_token: str
    token_type: str
    expires_in: int
    scope: str
    refresh_token: Optional[str] = None
    raw_response: dict = field(default_factory=dict)

    @classmethod
    def from_auth0_response(cls, data: dict) -> "LoginResponse":
        return cls(
            access_token=data.get("access_token", ""),
            id_token=data.get("id_token", ""),
            token_type=data.get("token_type", "Bearer"),
            expires_in=data.get("expires_in", 0),
            scope=data.get("scope", ""),
            refresh_token=data.get("refresh_token"),
            raw_response=data,
        )


@dataclass
class RefreshRequest:
    refresh_token: str
    client_id: Optional[str] = None

    def to_payload(self, client_id: str) -> dict:
        return {
            "grant_type": "refresh_token",
            "client_id": self.client_id or client_id,
            "refresh_token": self.refresh_token,
        }


@dataclass
class RefreshResponse:
    access_token: str
    id_token: str
    token_type: str
    expires_in: int
    scope: str
    refresh_token: Optional[str] = None
    raw_response: dict = field(default_factory=dict)

    @classmethod
    def from_auth0_response(cls, data: dict) -> "RefreshResponse":
        return cls(
            access_token=data.get("access_token", ""),
            id_token=data.get("id_token", ""),
            token_type=data.get("token_type", "Bearer"),
            expires_in=data.get("expires_in", 0),
            scope=data.get("scope", ""),
            refresh_token=data.get("refresh_token"),
            raw_response=data,
        )


@dataclass
class PasswordResetRequest:
    email: str
    connection: str = "Username-Password-Authentication"
    client_id: Optional[str] = None

    def to_payload(self, client_id: str) -> dict:
        return {
            "client_id": self.client_id or client_id,
            "email": self.email,
            "connection": self.connection,
        }


@dataclass
class PasswordResetResponse:
    email: str
    message: str
    success: bool
    raw_response: dict = field(default_factory=dict)

    @classmethod
    def from_auth0_response(cls, data: dict) -> "PasswordResetResponse":
        return cls(
            email=data.get("email", ""),
            message=data.get("message", ""),
            success="email" in data,
            raw_response=data,
        )


def normalize_email(email: str) -> str:
    local, _, domain = email.partition("@")
    local = local.lower()
    domain = domain.lower()
    if "+" in local:
        local = local.split("+")[0]
    return f"{local}@{domain}"


def normalize_password_strength(password: str) -> dict:
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)
    length = len(password)
    score = sum(
        [has_upper, has_lower, has_digit, has_special, length >= 8, length >= 12]
    )
    return {
        "length": length,
        "has_upper": has_upper,
        "has_lower": has_lower,
        "has_digit": has_digit,
        "has_special": has_special,
        "strength_score": score,
        "strength_label": "weak" if score < 3 else "medium" if score < 5 else "strong",
    }
