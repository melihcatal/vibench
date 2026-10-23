from dataclasses import dataclass


@dataclass
class UserRegistrationRequest:
    email: str
    password: str
    display_name: str


@dataclass
class UserLoginRequest:
    email: str
    password: str


@dataclass
class AuthTokenResponse:
    id_token: str
    refresh_token: str
    expires_in: int
    local_id: str


@dataclass
class RefreshTokenRequest:
    refresh_token: str


@dataclass
class PasswordResetRequest:
    email: str
