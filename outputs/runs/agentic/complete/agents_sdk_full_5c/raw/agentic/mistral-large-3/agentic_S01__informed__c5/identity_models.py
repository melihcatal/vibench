from pydantic import BaseModel
from typing import Optional

class RegisterUserRequest(BaseModel):
    email: str
    password: str
    username: Optional[str] = None

class RegisterUserResponse(BaseModel):
    user_id: str
    email: str
    created_at: str

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    id_token: str
    refresh_token: Optional[str] = None
    expires_in: int

class RefreshSessionRequest(BaseModel):
    refresh_token: str

class RefreshSessionResponse(BaseModel):
    access_token: str
    id_token: Optional[str] = None
    expires_in: int

class PasswordResetRequest(BaseModel):
    email: str

class PasswordResetResponse(BaseModel):
    success: bool
    message: str