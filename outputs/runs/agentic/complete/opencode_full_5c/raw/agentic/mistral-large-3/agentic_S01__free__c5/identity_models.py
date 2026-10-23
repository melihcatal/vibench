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


class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    client_id: Optional[str] = None
    audience: Optional[str] = None


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    id_token: str
    token_type: str
    expires_in: int


class RefreshTokenRequest(BaseModel):
    refresh_token: str
    client_id: Optional[str] = None


class RefreshTokenResponse(BaseModel):
    access_token: str
    id_token: str
    token_type: str
    expires_in: int


class PasswordResetRequest(BaseModel):
    email: EmailStr
    client_id: Optional[str] = None


class PasswordResetResponse(BaseModel):
    status: str
    message: str
