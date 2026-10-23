from pydantic import BaseModel, EmailStr, Field

class UserRegistrationRequest(BaseModel):
    email: EmailStr = Field(..., description='User email address')
    password: str = Field(..., min_length=8, description='User password')

class UserRegistrationResponse(BaseModel):
    user_id: str
    email: EmailStr
    created_at: str

class EmailPasswordLoginRequest(BaseModel):
    email: EmailStr = Field(..., description='User email')
    password: str = Field(..., description='User password')

class EmailPasswordLoginResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str
    user_id: str
