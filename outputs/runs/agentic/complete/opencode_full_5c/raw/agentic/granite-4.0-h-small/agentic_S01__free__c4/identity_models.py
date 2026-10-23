from typing import TypedDict, Optional


class RegisterRequest(TypedDict):
    email: str
    password: str
    # Optional extra fields the provider may accept
    extra: Optional[dict]


class RegisterResponse(TypedDict):
    user_id: str
    status: str
    message: str


class LoginRequest(TypedDict):
    email: str
    password: str
    # optional scopes, grant_type etc. for token response
    extra: Optional[dict]


class LoginResponse(TypedDict):
    access_token: str
    refresh_token: Optional[str]
    expires_in: int
    token_type: str


class RefreshRequest(TypedDict):
    refresh_token: str
    extra: Optional[dict]


class RefreshResponse(TypedDict):
    access_token: str
    expires_in: int


class ResetRequest(TypedDict):
    email: str
    extra: Optional[dict]


class ResetResponse(TypedDict):
    reset_id: str
    message: str
