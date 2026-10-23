from dataclasses import dataclass

@dataclass
class RegistrationRequest:
    email: str
    password: str

@dataclass
class RegistrationResponse:
    user_id: str
    message: str

@dataclass
class LoginRequest:
    email: str
    password: str

@dataclass
class LoginResponse:
    access_token: str
    refresh_token: str
    message: str

@dataclass
class RefreshTokenRequest:
    refresh_token: str

@dataclass
class RefreshTokenResponse:
    access_token: str
    message: str

@dataclass
class PasswordResetRequest:
    email: str

@dataclass
class PasswordResetResponse:
    message: str
