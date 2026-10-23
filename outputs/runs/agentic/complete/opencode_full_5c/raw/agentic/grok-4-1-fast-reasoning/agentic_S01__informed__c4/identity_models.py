from typing import TypedDict


class UserRegisterRequest(TypedDict):
    email: str
    password: str


class UserRegisterResponse(TypedDict):
    user_sub: str


class UserLoginRequest(TypedDict):
    email: str
    password: str


class UserLoginResponse(TypedDict):
    access_token: str
    id_token: str
    refresh_token: str
    expires_in: int


class RefreshTokenRequest(TypedDict):
    refresh_token: str


class RefreshTokenResponse(TypedDict):
    access_token: str
    id_token: str
    refresh_token: str
    expires_in: int


class PasswordResetRequest(TypedDict):
    email: str


class PasswordResetResponse(TypedDict):
    status: str
