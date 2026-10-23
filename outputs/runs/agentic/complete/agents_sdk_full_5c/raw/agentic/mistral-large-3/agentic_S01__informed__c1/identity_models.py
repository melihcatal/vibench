from typing import List, Dict, Optional
from pydantic import BaseModel


class RegisterUserRequest(BaseModel):
    email: str
    password: str
    username: Optional[str] = None


class RegisterUserResponse(BaseModel):
    user_id: str
    is_success: bool
    attributes: List[Dict[str, str]]


class LoginRequest(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
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
    email: str


class PasswordResetResponse(BaseModel):
    is_success: bool
    message: str