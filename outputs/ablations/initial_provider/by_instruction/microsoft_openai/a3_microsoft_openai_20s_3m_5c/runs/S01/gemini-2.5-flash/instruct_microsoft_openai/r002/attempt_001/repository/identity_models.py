import dataclasses

@dataclasses.dataclass
class RegisterUserRequest:
    email: str
    password: str

@dataclasses.dataclass
class RegisterUserResponse:
    user_id: str
    message: str

@dataclasses.dataclass
class LoginRequest:
    email: str
    password: str

@dataclasses.dataclass
class LoginResponse:
    access_token: str
    refresh_token: str
    expires_in: int

@dataclasses.dataclass
class RefreshSessionRequest:
    refresh_token: str

@dataclasses.dataclass
class RefreshSessionResponse:
    access_token: str
    expires_in: int

@dataclasses.dataclass
class PasswordResetRequest:
    email: str

@dataclasses.dataclass
class PasswordResetResponse:
    message: str
