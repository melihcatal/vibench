from typing import TypedDict, List, Dict, Any


class UserInfo(TypedDict):
    sub: str
    email: str
    email_verified: bool
    preferred_username: str
    name: str
    family_name: str
    given_name: str
    # Add other standard OIDC claims as needed


class TokenResponse(TypedDict):
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str
    id_token: str


class AuthorizationRequestParams(TypedDict):
    response_type: str
    client_id: str
    redirect_uri: str
    scope: str
    state: str  # optional
    code_challenge: str  # for PKCE flow
    code_challenge_method: str  # typically S256
