from pydantic import BaseModel


class RegisterUserRequest(BaseModel):
    email: str
    password: str


class LoginUserRequest(BaseModel):
    email: str
    password: str


class RefreshSessionRequest(BaseModel):
    token: str


class PasswordResetRequest(BaseModel):
    email: str


class UserResponse(BaseModel):
    user_id: str


class TokensResponse(BaseModel):
    tokens: str


class NewTokenResponse(BaseModel):
    new_token: str


class ErrorResponse(BaseModel):
    error: str


class PasswordResetMessageResponse(BaseModel):
    message: str