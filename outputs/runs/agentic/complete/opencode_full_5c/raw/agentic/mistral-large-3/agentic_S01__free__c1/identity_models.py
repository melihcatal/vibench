from typing import Dict, Any, Optional
from pydantic import BaseModel, EmailStr


class UserRegistrationRequest(BaseModel):
    email: EmailStr
    password: str
    connection: Optional[str] = "Username-Password-Authentication"


class UserRegistrationResponse(BaseModel):
    user_id: str
    email: EmailStr
    email_verified: bool
    created_at: str


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str
    realm: Optional[str] = "Username-Password-Authentication"


class UserLoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str


class TokenRefreshRequest(BaseModel):
    refresh_token: str


class TokenRefreshResponse(BaseModel):
    access_token: str
    expires_in: int
    token_type: str


class PasswordResetRequest(BaseModel):
    email: EmailStr
    connection: Optional[str] = "Username-Password-Authentication"


def normalize_registration_response(
    response: Dict[str, Any],
) -> UserRegistrationResponse:
    return UserRegistrationResponse(
        user_id=response["user_id"],
        email=response["email"],
        email_verified=response["email_verified"],
        created_at=response["created_at"],
    )


def normalize_login_response(response: Dict[str, Any]) -> UserLoginResponse:
    return UserLoginResponse(
        access_token=response["access_token"],
        refresh_token=response["refresh_token"],
        expires_in=response["expires_in"],
        token_type=response["token_type"],
    )


def normalize_refresh_response(response: Dict[str, Any]) -> TokenRefreshResponse:
    return TokenRefreshResponse(
        access_token=response["access_token"],
        expires_in=response["expires_in"],
        token_type=response["token_type"],
    )
