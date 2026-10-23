from dataclasses import dataclass

@dataclass
class RegisterUserRequest:
    email: str
    password: str

@dataclass
class RegisterUserResponse:
    id_token: str
    refresh_token: str
    expires_in: str
    local_id: str

@dataclass
class LoginUserRequest:
    email: str
    password: str

@dataclass
class LoginUserResponse:
    id_token: str
    refresh_token: str
    expires_in: str
    local_id: str

@dataclass
class RefreshSessionRequest:
    refresh_token: str

@dataclass
class RefreshSessionResponse:
    id_token: str
    refresh_token: str
    expires_in: str

@dataclass
class PasswordResetRequest:
    email: str

@dataclass
class PasswordResetResponse:
    email: str
