from pydantic import BaseModel, EmailStr
from typing import Optional

class UserRegistration(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class RefreshRequest(BaseModel):
    refresh_token: str

class PasswordResetRequest(BaseModel):
    email: EmailStr

class UserProfile(BaseModel):
    id: str
    email: EmailStr
    created_at: str

class SessionResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str
    user: UserProfile
