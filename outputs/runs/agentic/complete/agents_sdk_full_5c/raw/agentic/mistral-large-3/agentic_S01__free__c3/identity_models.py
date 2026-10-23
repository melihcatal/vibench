from dataclasses import dataclass
from typing import Optional


@dataclass
class RegisterUserRequest:
    email: str
    password: str
    display_name: Optional[str] = None


@dataclass
class RegisterUserError:
    code: Optional[str] = None
    message: Optional[str] = None


@dataclass
class RegisterUserResponse:
    success: bool
    user_id: Optional[str] = None
    email_verified: bool = False
    error: Optional[RegisterUserError] = None


@dataclass
class LoginRequest:
    email: str
    password: str


@dataclass
class LoginError:
    code: Optional[int] = None
    message: Optional[str] = None


@dataclass
class LoginResponse:
    success: bool
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_in: Optional[str] = None
    error: Optional[LoginError] = None


@dataclass
class RefreshSessionRequest:
    refresh_token: str


@dataclass
class RefreshSessionError:
    code: Optional[int] = None
    message: Optional[str] = None


@dataclass
class RefreshSessionResponse:
    success: bool
    id_token: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_in: Optional[str] = None
    error: Optional[RefreshSessionError] = None


@dataclass
class PasswordResetRequest:
    email: str


@dataclass
class PasswordResetError:
    code: Optional[int] = None
    message: Optional[str] = None


@dataclass
class PasswordResetResponse:
    success: bool
    email: Optional[str] = None
    error: Optional[PasswordResetError] = None