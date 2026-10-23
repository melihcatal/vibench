from typing import Dict, Any, TypedDict

class RegisterRequest(TypedDict):
    email: str
    password: str

class LoginRequest(TypedDict):
    email: str
    password: str

class RefreshRequest(TypedDict):
    refresh_token: str

class Tokens(TypedDict):
    access_token: str
    refresh_token: str

def normalize_tokens(data: Dict[str, Any]) -> Tokens:
    session = data.get("session", {})
    return Tokens(
        access_token=session.get("access_token", ""),
        refresh_token=session.get("refresh_token", "")
    )