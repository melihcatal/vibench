import dataclasses
from typing import Optional

@dataclasses.dataclass
class RegisterUserRequest:
    email: str
    password: str

@dataclasses.dataclass
class RegisterUserResponse:
    id_token: str
    refresh_token: str
    local_id: str

@dataclasses.dataclass
class LoginUserRequest:
    email: str
    password: str

@dataclasses.dataclass
class LoginUserResponse:
    id_token: str
    refresh_token: str
    local_id: str

@dataclasses.dataclass
class RefreshSessionRequest:
    refresh_token: str

@dataclasses.dataclass
class RefreshSessionResponse:
    id_token: str
    refresh_token: str
    local_id: str

@dataclasses.dataclass
class PasswordResetRequest:
    email: str

@dataclasses.dataclass
class PasswordResetResponse:
    email: str
