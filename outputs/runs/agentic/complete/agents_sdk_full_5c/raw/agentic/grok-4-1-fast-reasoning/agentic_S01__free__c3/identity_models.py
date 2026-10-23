from typing import TypedDict, Dict, Any, Optional

class RegisterPayload(TypedDict):
    email: str
    password: str

class Tokens(TypedDict):
    access_token: str
    refresh_token: str

class AuthUser(TypedDict):
    id: str
    email: str

class SessionResponse(TypedDict):
    user: Optional[AuthUser]
    session: Optional[Dict[str, Any]]