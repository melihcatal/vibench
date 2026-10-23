from typing import TypedDict

class RegisterRequest(TypedDict):
    email: str
    password: str
    locale: str

class RegisterResponse(TypedDict):
    user_id: str
    session_token: str  # short-lived access token
    refresh_token: str

class LoginRequest(TypedDict):
    email: str
    password: str

class LoginResponse(TypedDict):
    access_token: str
    refresh_token: str

class RefreshRequest(TypedDict):
    refresh_token: str

class RefreshResponse(TypedDict):
    access_token: str
