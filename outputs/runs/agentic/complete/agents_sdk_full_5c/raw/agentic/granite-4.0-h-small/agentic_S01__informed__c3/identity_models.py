from typing import TypedDict, List, Optional

class RegisterPayload(TypedDict):
    email: str
    password: str
    connection: str
    email_verified: bool

class RegisterResponse(TypedDict):
    user_id: str
    created_at: str
    user_metadata: Optional[Dict[str, Any]]
    app_metadata: Optional[Dict[str, Any]]


class LoginPayload(TypedDict):
    grant_type: str
    username: str
    password: str
    audience: str
    client_id: str
    scope: str
    # Optional extra fields for additional parameters can be added later

class LoginResponse(TypedDict):
    access_token: str
    id_token: str
    refresh_token: str
    expires_in: int
    token_type: str
    user: Optional[Dict[str, Any]]


class TokenRefreshPayload(TypedDict):
    grant_type: str
    refresh_token: str
    client_id: str
    audience: str
    scope: str  # optional

class TokenRefreshResponse(TypedDict):
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str


class PasswordResetStartPayload(TypedDict):
    email: str
    connection: str
