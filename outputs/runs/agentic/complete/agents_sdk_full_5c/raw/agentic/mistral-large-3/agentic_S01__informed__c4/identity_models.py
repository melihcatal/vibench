from typing import Dict, Any, Optional
from pydantic import BaseModel


class UserRegistrationRequest(BaseModel):
    email: str
    password: str
    connection: str = "Username-Password-Authentication"


class UserRegistrationResponse(BaseModel):
    user_id: str
    email: str
    email_verified: bool
    created_at: str

    @classmethod
    def from_auth0_response(cls, data: Dict[str, Any]) -> "UserRegistrationResponse":
        return cls(
            user_id=data["user_id"],
            email=data["email"],
            email_verified=data["email_verified"],
            created_at=data["created_at"]
        )


class LoginRequest(BaseModel):
    email: str
    password: str
    realm: str = "Username-Password-Authentication"


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str

    @classmethod
    def from_auth0_response(cls, data: Dict[str, Any]) -> "LoginResponse":
        return cls(
            access_token=data["access_token"],
            refresh_token=data["refresh_token"],
            expires_in=data["expires_in"],
            token_type=data["token_type"]
        )


class RefreshSessionRequest(BaseModel):
    refresh_token: str


class RefreshSessionResponse(BaseModel):
    access_token: str
    expires_in: int
    token_type: str

    @classmethod
    def from_auth0_response(cls, data: Dict[str, Any]) -> "RefreshSessionResponse":
        return cls(
            access_token=data["access_token"],
            expires_in=data["expires_in"],
            token_type=data["token_type"]
        )


class PasswordResetRequest(BaseModel):
    email: str
    connection: str = "Username-Password-Authentication"