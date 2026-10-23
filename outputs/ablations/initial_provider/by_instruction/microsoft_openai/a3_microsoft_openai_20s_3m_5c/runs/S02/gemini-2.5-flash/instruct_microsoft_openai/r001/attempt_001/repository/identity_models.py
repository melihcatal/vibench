from typing import TypedDict, Optional

class NormalizedClaims(TypedDict):
    id: str
    email: str
    first_name: Optional[str]
    last_name: Optional[str]
    display_name: Optional[str]
    tenant_id: Optional[str]

class OAuthTokens(TypedDict):
    access_token: str
    token_type: str
    expires_in: int
    scope: str
    refresh_token: Optional[str]
    id_token: Optional[str]

# You can add more models here as needed for request/response bodies or other data structures.
