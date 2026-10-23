from pydantic import BaseModel

# Define local request, response, and normalization helpers for Email/Password Account Lifecycle
class User(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    uid: str
    email: str

class TokenResponse(BaseModel):
    token: str

class RefreshResponse(BaseModel):
    access_token: str
    refresh_token: str