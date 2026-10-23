from dataclasses import dataclass

@dataclass
class UserLoginRequest:
    email: str
    password: str
    
@dataclass
class UserLoginResponse:
    access_token: str
    refresh_token: str
    id_token: str
    expires_in: int
    token_type: str

@dataclass
class TokenRefreshRequest:
    refresh_token: str

@dataclass
class TokenRefreshResponse:
    access_token: str
    id_token: str
    expires_in: int
    token_type: str

@dataclass
class PasswordResetRequest:
    email: str
