from typing import TypedDict, Dict, Any

class AuthPayload(TypedDict):
    email: str
    password: str

class User(TypedDict, total=False):
    id: str
    email: str

class Session(TypedDict, total=False):
    access_token: str
    refresh_token: str
    expires_in: int

class AuthResponse(TypedDict, total=False):
    user: User
    session: Session
