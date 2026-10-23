from pydantic import BaseModel
from typing import Optional, Dict, Any


class RegisterUserRequest(BaseModel):
    email: str
    password: str
    connection: str = "Username-Password-Authentication"
    given_name: Optional[str] = None
    family_name: Optional[str] = None


class RegisterUserResponse(BaseModel):
    id: str
    email: str
    email_verified: bool


class LoginRequest(BaseModel):
    username: str
    password: str
    audience: str
    scope: str = "openid profile email"
    grant_type: str = "password"
    client_id: str
    client_secret: str


class LoginResponse(BaseModel):
    access_token: str
    id_token: str
    scope: str
    expires_in: int
    token_type: str
    refresh_token: Optional[str] = None


class RefreshTokenRequest(BaseModel):
    grant_type: str = "refresh_token"
    client_id: str
    client_secret: str
    refresh_token: str


class RefreshTokenResponse(BaseModel):
    access_token: str
    id_token: str
    scope: str
    expires_in: int
    token_type: str


class PasswordResetRequest(BaseModel):
    email: str
    connection: str = "Username-Password-Authentication"
    client_id: str
