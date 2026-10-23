from dataclasses import dataclass

@dataclass
class OAuthCallbackRequest:
    code: str
    state: str

@dataclass
class OAuthCallbackResponse:
    access_token: str
    refresh_token: str
    id_token: str
    expires_in: int

@dataclass
class ProfileClaimsRequest:
    access_token: str

@dataclass
class ProfileClaimsResponse:
    user_id: str
    display_name: str
    email: str