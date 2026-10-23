from pydantic import BaseModel, Field
from typing import Optional


class UserIdentity(BaseModel):
    uid: str
    email: str
    display_name: Optional[str] = None
    photo_url: Optional[str] = None
    email_verified: bool = False


class AuthRequest(BaseModel):
    email: str
    password: str


class AuthResponse(BaseModel):
    id_token: str = Field(..., alias="idToken")
    refresh_token: str = Field(..., alias="refreshToken")
    expires_in: str = Field(..., alias="expiresIn")
    local_id: str = Field(..., alias="localId")
    is_new_user: bool = Field(False, alias="isNewUser")


class PasswordResetRequest(BaseModel):
    email: str
