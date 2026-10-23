from typing import Optional, Dict, Any

class UserRegistrationRequest:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

class UserRegistrationResponse:
    def __init__(self, user_id: str, email: str, success: bool = True, error: Optional[str] = None):
        self.user_id = user_id
        self.email = email
        self.success = success
        self.error = error

class UserLoginRequest:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

class UserLoginResponse:
    def __init__(
        self,
        access_token: Optional[str] = None,
        id_token: Optional[str] = None,
        refresh_token: Optional[str] = None,
        expires_in: Optional[int] = None,
        success: bool = True,
        error: Optional[str] = None,
        raw_response: Optional[Dict[str, Any]] = None
    ):
        self.access_token = access_token
        self.id_token = id_token
        self.refresh_token = refresh_token
        self.expires_in = expires_in
        self.success = success
        self.error = error
        self.raw_response = raw_response

class RefreshSessionResponse:
    def __init__(
        self,
        access_token: Optional[str] = None,
        id_token: Optional[str] = None,
        refresh_token: Optional[str] = None,
        expires_in: Optional[int] = None,
        success: bool = True,
        error: Optional[str] = None
    ):
        self.access_token = access_token
        self.id_token = id_token
        self.refresh_token = refresh_token
        self.expires_in = expires_in
        self.success = success
        self.error = error

class PasswordResetRequest:
    def __init__(self, email: str):
        self.email = email

class PasswordResetResponse:
    def __init__(self, success: bool = True, message: Optional[str] = None, error: Optional[str] = None):
        self.success = success
        self.message = message
        self.error = error
