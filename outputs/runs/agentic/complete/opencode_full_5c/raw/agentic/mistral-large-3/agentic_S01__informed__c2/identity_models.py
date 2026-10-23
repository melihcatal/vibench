from typing import Dict, Any, Optional
from pydantic import BaseModel


class UserRegistrationRequest(BaseModel):
    email: str
    password: str


class UserLoginRequest(BaseModel):
    email: str
    password: str


class TokenRefreshRequest(BaseModel):
    refresh_token: str


class PasswordResetRequest(BaseModel):
    email: str


class AuthResponse(BaseModel):
    id_token: str
    refresh_token: str
    expires_in: str
    local_id: Optional[str] = None
    email: Optional[str] = None
    kind: Optional[str] = None


class PasswordResetResponse(BaseModel):
    email: str
    kind: str


class IdentityError(Exception):
    def __init__(self, message: str, code: Optional[int] = None):
        self.message = message
        self.code = code
        super().__init__(message)


def normalize_auth_response(response: Dict[str, Any]) -> AuthResponse:
    return AuthResponse(
        id_token=response.get("idToken"),
        refresh_token=response.get("refreshToken"),
        expires_in=response.get("expiresIn"),
        local_id=response.get("localId"),
        email=response.get("email"),
        kind=response.get("kind"),
    )


def normalize_password_reset_response(
    response: Dict[str, Any],
) -> PasswordResetResponse:
    return PasswordResetResponse(email=response.get("email"), kind=response.get("kind"))
