from dataclasses import dataclass

@dataclass
class UserRegisterRequest:
    """Payload for user registration request."""
    username: str
    password: str
    user_attributes: dict = None

@dataclass
class TokenResponse:
    """Response containing authentication tokens."""
    access_token: str
    id_token: str
    refresh_token: str

@dataclass
class RefreshSessionRequest:
    refresh_token: str

@dataclass
class RefreshSessionResponse:
    access_token: str
    id_token: str
    refresh_token: str

@dataclass
class StartPasswordResetRequest:
    email: str

@dataclass
class ConfirmPasswordResetRequest:
    email: str
    confirmation_code: str
    new_password: str
