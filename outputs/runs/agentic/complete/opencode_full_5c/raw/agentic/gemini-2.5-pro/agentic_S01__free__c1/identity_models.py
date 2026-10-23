from pydantic import BaseModel, Field
from typing import Optional


class UserRegistration(BaseModel):
    email: str
    password: str
    display_name: Optional[str] = None


class UserLogin(BaseModel):
    email: str
    password: str


class LoginResponse(BaseModel):
    id_token: str = Field(..., alias="idToken")
    refresh_token: str = Field(..., alias="refreshToken")
    expires_in: str = Field(..., alias="expiresIn")
    local_id: str = Field(..., alias="localId")


class RefreshResponse(BaseModel):
    access_token: str = Field(..., alias="access_token")
    expires_in: str = Field(..., alias="expires_in")
    token_type: str = Field(..., alias="token_type")
    refresh_token: str = Field(..., alias="refresh_token")
    id_token: str = Field(..., alias="id_token")
    user_id: str = Field(..., alias="user_id")
    project_id: str = Field(..., alias="project_id")


class ProfileData(BaseModel):
    user_id: str
    profile_text: str
    notes: dict
