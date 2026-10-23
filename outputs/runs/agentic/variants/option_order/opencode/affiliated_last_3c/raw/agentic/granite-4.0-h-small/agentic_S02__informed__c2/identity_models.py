from typing import TypedDict, Optional


class OAuthAuthorizationResponse(TypedDict):
    code: str
    state: str


class OAuthTokenResponse(TypedDict):
    access_token: str
    id_token: str
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None


class UserProfile(TypedDict):
    sub: str
    email: str
    name: Optional[str] = None
    picture: Optional[str] = None
    provider: str
