from typing import Optional, Dict
from pydantic import BaseModel, EmailStr

class UserRegistration(BaseModel):
    email: EmailStr
    password: str
    
class LoginCredentials(BaseModel):
    email: EmailStr
    password: str

class RefreshRequest(BaseModel):
    refresh_token: str

class PasswordResetRequest(BaseModel):
    email: EmailStr

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    id_token: str
    token_type: str
    expires_in: int

class User(BaseModel):
    user_id: str
    username: str
    attributes: Dict
