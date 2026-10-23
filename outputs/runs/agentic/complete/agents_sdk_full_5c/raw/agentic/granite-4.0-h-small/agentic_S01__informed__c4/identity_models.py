from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    # optional fields can be added here

class UserResponse(BaseModel):
    user_id: str
    email: EmailStr
    created_at: str
    # provider-specific extras omitted for brevity

class TokenResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str | None = None
