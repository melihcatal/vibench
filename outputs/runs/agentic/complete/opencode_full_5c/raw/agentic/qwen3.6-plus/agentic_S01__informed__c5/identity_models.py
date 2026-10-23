import os
from dataclasses import dataclass, field, asdict
from typing import Optional, Any


@dataclass
class RegisterUserRequest:
    email: str
    password: str
    connection: str = "Username-Password-Authentication"
    user_metadata: dict = field(default_factory=dict)
    app_metadata: dict = field(default_factory=dict)

    def to_auth0_payload(self) -> dict:
        payload = {
            "email": self.email,
            "password": self.password,
            "connection": self.connection,
        }
        if self.user_metadata:
            payload["user_metadata"] = self.user_metadata
        if self.app_metadata:
            payload["app_metadata"] = self.app_metadata
        return payload


@dataclass
class RegisterUserResponse:
    user_id: str
    email: str
    email_verified: bool
    created_at: str
    identities: list = field(default_factory=list)

    @classmethod
    def from_auth0_response(cls, data: dict) -> "RegisterUserResponse":
        return cls(
            user_id=data.get("user_id", ""),
            email=data.get("email", ""),
            email_verified=data.get("email_verified", False),
            created_at=data.get("created_at", ""),
            identities=data.get("identities", []),
        )


@dataclass
class LoginRequest:
    email: str
    password: str
    audience: Optional[str] = None
    scope: str = "openid profile email"

    def to_auth0_payload(self, client_id: str) -> dict:
        payload = {
            "grant_type": "password",
            "username": self.email,
            "password": self.password,
            "client_id": client_id,
            "scope": self.scope,
        }
        if self.audience:
            payload["audience"] = self.audience
        return payload


@dataclass
class LoginResponse:
    access_token: str
    id_token: str
    token_type: str = "Bearer"
    expires_in: int = 0
    refresh_token: Optional[str] = None
    scope: Optional[str] = None

    @classmethod
    def from_auth0_response(cls, data: dict) -> "LoginResponse":
        return cls(
            access_token=data.get("access_token", ""),
            id_token=data.get("id_token", ""),
            token_type=data.get("token_type", "Bearer"),
            expires_in=data.get("expires_in", 0),
            refresh_token=data.get("refresh_token"),
            scope=data.get("scope"),
        )


@dataclass
class RefreshSessionRequest:
    refresh_token: str
    audience: Optional[str] = None
    scope: Optional[str] = None

    def to_auth0_payload(self, client_id: str) -> dict:
        payload = {
            "grant_type": "refresh_token",
            "client_id": client_id,
            "refresh_token": self.refresh_token,
        }
        if self.audience:
            payload["audience"] = self.audience
        if self.scope:
            payload["scope"] = self.scope
        return payload


@dataclass
class RefreshSessionResponse:
    access_token: str
    id_token: str
    token_type: str = "Bearer"
    expires_in: int = 0
    scope: Optional[str] = None

    @classmethod
    def from_auth0_response(cls, data: dict) -> "RefreshSessionResponse":
        return cls(
            access_token=data.get("access_token", ""),
            id_token=data.get("id_token", ""),
            token_type=data.get("token_type", "Bearer"),
            expires_in=data.get("expires_in", 0),
            scope=data.get("scope"),
        )


@dataclass
class PasswordResetRequest:
    email: str
    connection: str = "Username-Password-Authentication"

    def to_auth0_payload(self, client_id: str) -> dict:
        return {
            "client_id": client_id,
            "email": self.email,
            "connection": self.connection,
        }


@dataclass
class PasswordResetResponse:
    email: str
    connection: str
    ticket_url: Optional[str] = None
    message: str = ""

    @classmethod
    def from_auth0_response(
        cls, data: dict, email: str, connection: str
    ) -> "PasswordResetResponse":
        return cls(
            email=email,
            connection=connection,
            ticket_url=data.get("ticket_url"),
            message=data.get("message", "Password reset email sent"),
        )


def normalize_auth0_error(response_data: dict) -> dict:
    return {
        "error": response_data.get(
            "error", response_data.get("errorCode", "unknown_error")
        ),
        "error_description": response_data.get(
            "error_description", response_data.get("description", "")
        ),
        "status_code": response_data.get("statusCode"),
    }
