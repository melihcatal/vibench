from pydantic import BaseModel, Field
from typing import Optional

class UserRegistrationRequest(BaseModel):
    email: str
    password: str
    display_name: Optional[str] = None

class UserRegistrationResponse(BaseModel):
    uid: str
    email: str
    display_name: Optional[str] = None

class UserLoginRequest(BaseModel):
    email: str
    password: str

class UserLoginResponse(BaseModel):
    id_token: str = Field(..., alias="idToken")
    refresh_token: str = Field(..., alias="refreshToken")
    expires_in: str = Field(..., alias="expiresIn")
    local_id: str = Field(..., alias="localId")

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class RefreshTokenResponse(BaseModel):
    id_token: str = Field(..., alias="id_token")
    refresh_token: str = Field(..., alias="refresh_token")
    expires_in: str = Field(..., alias="expires_in")
    token_type: str = Field(..., alias="token_type")
    user_id: str = Field(..., alias="user_id")

class PasswordResetRequest(BaseModel):
    email: str

class PasswordResetResponse(BaseModel):
    reset_link: str
