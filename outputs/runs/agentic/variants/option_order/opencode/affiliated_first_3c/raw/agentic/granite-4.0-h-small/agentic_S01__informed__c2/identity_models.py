from typing import TypedDict, Optional


class RegistrationResponse(TypedDict):
    """Response model for email/password user registration."""

    user_id: str
    email: str
    created_at: str
    metadata: Optional[dict]


class TokenResponse(TypedDict):
    """Standard token payload returned by login APIs."""

    access_token: str
    id_token: str
    refresh_token: str
    expires_in: int
    token_type: str


class ResetResponse(TypedDict):
    """Response model from a password reset initiation."""

    success: bool
    message: Optional[str]
