from pydantic import BaseModel, EmailStr

class UserCredentials(BaseModel):
    email: EmailStr
    password: str

class Session(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int

class UserRegistrationResponse(BaseModel):
    id: str
    email: EmailStr
