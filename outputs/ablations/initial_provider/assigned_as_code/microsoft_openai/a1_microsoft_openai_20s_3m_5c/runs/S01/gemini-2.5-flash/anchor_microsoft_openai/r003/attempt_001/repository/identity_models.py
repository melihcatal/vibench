import dataclasses

@dataclasses.dataclass
class UserCredentials:
    email: str
    password: str

@dataclasses.dataclass
class AuthTokens:
    id_token: str
    refresh_token: str
    expires_in: int
    local_id: str

@dataclasses.dataclass
class RefreshTokenRequest:
    refresh_token: str

@dataclasses.dataclass
class PasswordResetRequest:
    email: str
