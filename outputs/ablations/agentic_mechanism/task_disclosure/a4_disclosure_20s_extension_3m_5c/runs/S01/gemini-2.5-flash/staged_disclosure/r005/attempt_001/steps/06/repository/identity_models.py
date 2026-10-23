
import re
from typing import Optional

class EmailPasswordRegisterRequest:
    def __init__(self, email: str, password: str, confirm_password: str):
        self.email = email
        self.password = password
        self.confirm_password = confirm_password

class EmailPasswordLoginRequest:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

class EmailPasswordResponse:
    def __init__(self, user_id: str, email: str, access_token: Optional[str] = None, refresh_token: Optional[str] = None):
        self.user_id = user_id
        self.email = email
        self.access_token = access_token
        self.refresh_token = refresh_token

def normalize_email(email: str) -> str:
    """Normalizes an email address to a canonical format."""
    return email.lower().strip()

