from pydantic import BaseModel

class RegisterUserRequest(BaseModel):
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class RefreshSessionRequest(BaseModel):
    refresh_token: str

class PasswordResetRequest(BaseModel):
    email: str