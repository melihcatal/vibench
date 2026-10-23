from typing import Optional
from pydantic import BaseModel, Field


class UserRegistrationRequest(BaseModel):
    email: str
    password: str


class UserLoginRequest(BaseModel):
    email: str
    password: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class PasswordResetRequest(BaseModel):
    email: str


class AuthResponse(BaseModel):
    id_token: str = Field(..., alias="idToken")
    refresh_token: str = Field(..., alias="refreshToken")
    expires_in: str = Field(..., alias="expiresIn")
    local_id: str = Field(..., alias="localId")

    class Config:
        populate_by_name = True


class UserRecord(BaseModel):
    uid: str
    email: Optional[str] = None
    email_verified: bool
    display_name: Optional[str] = None
    disabled: bool
