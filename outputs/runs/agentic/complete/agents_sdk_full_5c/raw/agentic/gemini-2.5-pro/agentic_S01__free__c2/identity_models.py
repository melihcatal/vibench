from pydantic import BaseModel, Field
from typing import Optional


class UserCreateRequest(BaseModel):
    email: str
    password: str
    display_name: Optional[str] = None


class UserLoginRequest(BaseModel):
    email: str
    password: str


class TokenRefreshRequest(BaseModel):
    refresh_token: str


class PasswordResetRequest(BaseModel):
    email: str


class AuthResponse(BaseModel):
    id_token: str = Field(..., alias="idToken")
    refresh_token: str = Field(..., alias="refreshToken")
    expires_in: str = Field(..., alias="expiresIn")
    local_id: str = Field(..., alias="localId")
    is_new_user: bool = Field(False, alias="isNewUser")


class User(BaseModel):
    uid: str
    email: str
    display_name: Optional[str] = None
