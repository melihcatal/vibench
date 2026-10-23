from dataclasses import dataclass

@dataclass
class OAuthFlow:
    state: str
    auth_uri: str

@dataclass
class TokenResponse:
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str

@dataclass
class ProfileResponse:
    user_id: str
    display_name: str
    email: str