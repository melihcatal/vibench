from typing import Optional, Dict, Any

class UserRegistrationRequest:
    def __init__(self, email: str, password: str, metadata: Optional[Dict[str, Any]] = None):
        self.email = email
        self.password = password
        self.metadata = metadata if metadata is not None else {}

class UserLoginRequest:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

class AuthTokens:
    def __init__(self, id_token: str, access_token: str, refresh_token: Optional[str] = None, expires_in: Optional[int] = None):
        self.id_token = id_token
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expires_in = expires_in

class ServiceResponse:
    def __init__(self, success: bool, message: str, data: Optional[Dict[str, Any]] = None):
        self.success = success
        self.message = message
        self.data = data if data is not None else {}

def normalize_email(email: str) -> str:
    """
    Normalizes an email address (e.g., converts to lowercase).
    """
    return email.lower().strip()
