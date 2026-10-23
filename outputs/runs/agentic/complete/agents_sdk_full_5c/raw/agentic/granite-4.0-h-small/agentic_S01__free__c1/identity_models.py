from typing import TypedDict, Optional

class CreateUserResponse(TypedDict):
    success: bool
    user_id: str
    email: str
    created_at: str
    metadata: Optional[dict]

class LoginResponse(TypedDict):
    access_token: str
    refresh_token: str
    id_token: Optional[str]
    expires_in: int
    token_type: str

class PasswordResetResponse(TypedDict):
    reset_ticket_id: str
    email: str
    request_id: str
