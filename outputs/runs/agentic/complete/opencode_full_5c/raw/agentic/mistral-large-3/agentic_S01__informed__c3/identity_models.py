from typing import Dict, Any, Optional
from pydantic import BaseModel, EmailStr


class UserRegistrationRequest(BaseModel):
    email: EmailStr
    password: str
    user_attributes: Optional[Dict[str, Any]] = None


class UserRegistrationResponse(BaseModel):
    user_sub: str
    user_confirmed: bool
    code_delivery_details: Optional[Dict[str, Any]] = None


class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserLoginResponse(BaseModel):
    access_token: str
    id_token: str
    refresh_token: str
    expires_in: int


class RefreshSessionRequest(BaseModel):
    refresh_token: str


class RefreshSessionResponse(BaseModel):
    access_token: str
    id_token: str
    expires_in: int


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetResponse(BaseModel):
    code_delivery_details: Optional[Dict[str, Any]] = None
