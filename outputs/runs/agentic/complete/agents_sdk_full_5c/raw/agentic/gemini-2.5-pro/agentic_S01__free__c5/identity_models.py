from typing import Optional
from pydantic import BaseModel, EmailStr

class UserRegistration(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class PasswordResetRequest(BaseModel):
    email: EmailStr

class SessionRefresh(BaseModel):
    refresh_token: str

class AuthProviderUser(BaseModel):
    uid: str
    email: Optional[str] = None
    id_token: str
    refresh_token: str

class RefreshedSession(BaseModel):
    id_token: str
    refresh_token: str
    user_id: str
