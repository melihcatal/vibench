from typing import TypedDict, Dict, Any


class RegisterInput(TypedDict):
    email: str
    password: str


class LoginInput(TypedDict):
    email: str
    password: str


class RefreshInput(TypedDict):
    refresh_token: str


class PasswordResetInput(TypedDict):
    email: str


class AuthSession(TypedDict):
    access_token: str
    refresh_token: str
    user_id: str
