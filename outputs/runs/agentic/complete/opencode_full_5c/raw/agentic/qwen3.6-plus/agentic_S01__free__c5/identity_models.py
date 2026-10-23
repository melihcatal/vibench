from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, Any, List
from datetime import datetime


@dataclass
class RegisterUserRequest:
    email: str
    password: str
    connection: str = "Username-Password-Authentication"
    given_name: Optional[str] = None
    family_name: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    def to_auth0_payload(self) -> Dict[str, Any]:
        payload = {
            "email": self.email,
            "password": self.password,
            "connection": self.connection,
        }
        if self.given_name or self.family_name:
            payload["name"] = (
                f"{self.given_name or ''} {self.family_name or ''}".strip()
            )
        if self.metadata:
            payload["user_metadata"] = self.metadata
        return payload


@dataclass
class RegisterUserResponse:
    user_id: str
    email: str
    email_verified: bool
    created_at: str
    identities: List[Dict[str, Any]] = field(default_factory=list)
    user_metadata: Optional[Dict[str, Any]] = None

    @classmethod
    def from_auth0_response(cls, data: Dict[str, Any]) -> "RegisterUserResponse":
        return cls(
            user_id=data.get("user_id", ""),
            email=data.get("email", ""),
            email_verified=data.get("email_verified", False),
            created_at=data.get("created_at", ""),
            identities=data.get("identities", []),
            user_metadata=data.get("user_metadata"),
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class LoginRequest:
    email: str
    password: str
    audience: str
    scope: str = "openid profile email offline_access"
    grant_type: str = "http://auth0.com/oauth/grant-type/password-realm"
    realm: str = "Username-Password-Authentication"

    def to_auth0_payload(self) -> Dict[str, Any]:
        return {
            "grant_type": self.grant_type,
            "username": self.email,
            "password": self.password,
            "audience": self.audience,
            "scope": self.scope,
            "realm": self.realm,
        }


@dataclass
class LoginResponse:
    access_token: str
    id_token: str
    refresh_token: Optional[str]
    token_type: str
    expires_in: int
    scope: str

    @classmethod
    def from_auth0_response(cls, data: Dict[str, Any]) -> "LoginResponse":
        return cls(
            access_token=data.get("access_token", ""),
            id_token=data.get("id_token", ""),
            refresh_token=data.get("refresh_token"),
            token_type=data.get("token_type", "Bearer"),
            expires_in=data.get("expires_in", 86400),
            scope=data.get("scope", ""),
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class RefreshTokenRequest:
    refresh_token: str
    client_id: str
    grant_type: str = "refresh_token"

    def to_auth0_payload(self) -> Dict[str, Any]:
        return {
            "grant_type": self.grant_type,
            "refresh_token": self.refresh_token,
            "client_id": self.client_id,
        }


@dataclass
class RefreshTokenResponse:
    access_token: str
    id_token: str
    token_type: str
    expires_in: int
    scope: str

    @classmethod
    def from_auth0_response(cls, data: Dict[str, Any]) -> "RefreshTokenResponse":
        return cls(
            access_token=data.get("access_token", ""),
            id_token=data.get("id_token", ""),
            token_type=data.get("token_type", "Bearer"),
            expires_in=data.get("expires_in", 86400),
            scope=data.get("scope", ""),
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class PasswordResetRequest:
    email: str
    connection: str = "Username-Password-Authentication"
    client_id: Optional[str] = None

    def to_auth0_payload(self) -> Dict[str, Any]:
        payload = {
            "email": self.email,
            "connection": self.connection,
        }
        if self.client_id:
            payload["client_id"] = self.client_id
        return payload


@dataclass
class PasswordResetResponse:
    email: str
    reset_sent: bool
    message: str

    @classmethod
    def from_auth0_response(cls, data: Dict[str, Any]) -> "PasswordResetResponse":
        return cls(
            email=data.get("email", ""),
            reset_sent=True,
            message=data.get("message", "Password reset email sent"),
        )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class IdentityError:
    status_code: int
    error: str
    error_description: str
    raw_response: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status_code": self.status_code,
            "error": self.error,
            "error_description": self.error_description,
        }
