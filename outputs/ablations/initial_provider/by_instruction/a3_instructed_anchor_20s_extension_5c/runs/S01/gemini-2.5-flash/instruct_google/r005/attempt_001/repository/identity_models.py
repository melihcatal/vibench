
import dataclasses
import typing

@dataclasses.dataclass
class UserRegistrationRequest:
    email: str
    password: str
    return_secure_token: bool = True

@dataclasses.dataclass
class UserRegistrationResponse:
    id_token: str
    email: str
    refresh_token: str
    expires_in: str
    local_id: str

@dataclasses.dataclass
class UserLoginRequest:
    email: str
    password: str
    return_secure_token: bool = True

@dataclasses.dataclass
class UserLoginResponse:
    id_token: str
    email: str
    refresh_token: str
    expires_in: str
    local_id: str
    registered: bool

@dataclasses.dataclass
class RefreshSessionRequest:
    grant_type: str = "refresh_token"
    refresh_token: str = ""

@dataclasses.dataclass
class RefreshSessionResponse:
    id_token: str
    refresh_token: str
    expires_in: str
    token_type: str

@dataclasses.dataclass
class PasswordResetRequest:
    request_type: str = "PASSWORD_RESET"
    email: str = ""

@dataclasses.dataclass
class PasswordResetResponse:
    email: str

