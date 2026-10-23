from typing import TypedDict, Dict, Any


class RegisterRequest(TypedDict):
    email: str
    password: str


class LoginRequest(TypedDict):
    email: str
    password: str


class RefreshRequest(TypedDict):
    refresh_token: str


class AuthResponse(TypedDict):
    user: Dict[str, Any]
    session: Dict[str, Any]
