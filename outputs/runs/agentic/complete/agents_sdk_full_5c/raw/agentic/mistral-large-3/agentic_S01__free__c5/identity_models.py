from pydantic import BaseModel

class RegisterRequest(BaseModel):
    email: str
    password: str
    display_name: str

class RegisterResponse(BaseModel):
    user_id: str
    email: str
    display_name: str

class LoginRequest(BaseModel):
    email: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    user_id: str

class RefreshSessionRequest(BaseModel):
    refresh_token: str

class RefreshSessionResponse(BaseModel):
    access_token: str
    refresh_token: str

class PasswordResetRequest(BaseModel):
    email: str

class PasswordResetResponse(BaseModel):
    reset_link: str
    email: str