from typing import TypedDict, Optional

class UserClaims(TypedDict):
    """Normalized user profile claims."""
    user_id: str
    email: Optional[str]
    email_verified: Optional[bool]
    name: Optional[str]
    nickname: Optional[str]
    picture: Optional[str]

class TokenResponse(TypedDict):
    """Normalized token response."""
    access_token: str
    id_token: str
    scope: str
    expires_in: int
    token_type: str
