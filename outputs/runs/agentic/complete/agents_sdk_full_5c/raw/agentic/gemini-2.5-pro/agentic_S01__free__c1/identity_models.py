from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class UserRegistration(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class RefreshRequest(BaseModel):
    refresh_token: str

class PasswordResetRequest(BaseModel):
    email: EmailStr

class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    user_id: str
    expires_in: int
