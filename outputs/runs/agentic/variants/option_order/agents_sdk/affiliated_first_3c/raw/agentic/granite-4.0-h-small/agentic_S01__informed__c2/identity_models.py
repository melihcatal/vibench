from pydantic import BaseModel, EmailStr, Field

UserId = str
AccessToken = str
RefreshToken = str


class UserCreationRequest(BaseModel):
    username: EmailStr
    password: str = Field(min_length=8, description='Plain-text password')

class UserCreationResponse(BaseModel):
    user_id: UserId
    access_token: AccessToken
    refresh_token: RefreshToken


class EmailPasswordLoginRequest(BaseModel):
    username: EmailStr
    password: str

class EmailPasswordLoginResponse(BaseModel):
    access_token: AccessToken
    refresh_token: RefreshToken


class RefreshTokenRequest(BaseModel):
    token: RefreshToken

class RefreshTokenResponse(BaseModel):
    access_token: AccessToken
    refresh_token: RefreshToken | None = None


class InitiatePasswordResetRequest(BaseModel):
    username: EmailStr

class InitiatePasswordResetResponse(BaseModel):
    message: str
    # optional: verification_code: str | None = None
