from dataclasses import dataclass
from typing import Optional

@dataclass
class UserRegistration:
    email: str
    password: str
    display_name: Optional[str] = None

@dataclass
class UserCredentials:
    email: str
    password: str

@dataclass
class LoginResponse:
    id_token: str
    refresh_token: str
    expires_in: str
    local_id: str

@dataclass
class RefreshResponse:
    id_token: str
    refresh_token: str
    expires_in: str
    token_type: str
    user_id: str
