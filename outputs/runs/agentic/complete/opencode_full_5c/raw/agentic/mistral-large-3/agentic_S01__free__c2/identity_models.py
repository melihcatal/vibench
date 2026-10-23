from typing import Dict, Any, Optional
from pydantic import BaseModel, EmailStr


class UserRegistrationRequest(BaseModel):
    email: EmailStr
    password: str
    connection: Optional[str] = None


class UserRegistrationResponse(BaseModel):
    user_id: str
    email: EmailStr
    email_verified: bool


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    client_id: Optional[str] = None
    client_secret: Optional[str] = None
    audience: Optional[str] = None
    scope: Optional[str] = "openid profile email"


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    id_token: str
    token_type: str
    expires_in: int


class RefreshSessionRequest(BaseModel):
    refresh_token: str
    client_id: Optional[str] = None
    client_secret: Optional[str] = None


class RefreshSessionResponse(BaseModel):
    access_token: str
    id_token: str
    token_type: str
    expires_in: int


class PasswordResetRequest(BaseModel):
    email: EmailStr
    connection: Optional[str] = None


class PasswordResetResponse(BaseModel):
    status: str
    message: str


def normalize_registration_response(
    response: Dict[str, Any],
) -> UserRegistrationResponse:
    return UserRegistrationResponse(
        user_id=response["_id"],
        email=response["email"],
        email_verified=response["email_verified"],
    )


def normalize_login_response(response: Dict[str, Any]) -> LoginResponse:
    return LoginResponse(
        access_token=response["access_token"],
        refresh_token=response["refresh_token"],
        id_token=response["id_token"],
        token_type=response["token_type"],
        expires_in=response["expires_in"],
    )


def normalize_refresh_response(response: Dict[str, Any]) -> RefreshSessionResponse:
    return RefreshSessionResponse(
        access_token=response["access_token"],
        id_token=response["id_token"],
        token_type=response["token_type"],
        expires_in=response["expires_in"],
    )
