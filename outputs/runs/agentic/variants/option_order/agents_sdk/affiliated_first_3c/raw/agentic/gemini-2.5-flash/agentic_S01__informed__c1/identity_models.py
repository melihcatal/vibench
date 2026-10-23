from typing import Optional, Dict, Any

class UserRegistrationRequest:
    email: str
    password: str

    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

class UserRegistrationResponse:
    uid: Optional[str]
    email: Optional[str]
    message: Optional[str]
    error: Optional[str]

    def __init__(self, uid: Optional[str] = None, email: Optional[str] = None,
                 message: Optional[str] = None, error: Optional[str] = None):
        self.uid = uid
        self.email = email
        self.message = message
        self.error = error

class UserLoginRequest:
    email: str
    password: str

    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

class UserLoginResponse:
    id_token: Optional[str]
    refresh_token: Optional[str]
    expires_in: Optional[str]
    local_id: Optional[str]
    message: Optional[str]
    error: Optional[str]

    def __init__(self, id_token: Optional[str] = None, refresh_token: Optional[str] = None,
                 expires_in: Optional[str] = None, local_id: Optional[str] = None,
                 message: Optional[str] = None, error: Optional[str] = None):
        self.id_token = id_token
        self.refresh_token = refresh_token
        self.expires_in = expires_in
        self.local_id = local_id
        self.message = message
        self.error = error

class SessionRefreshRequest:
    refresh_token: str

    def __init__(self, refresh_token: str):
        self.refresh_token = refresh_token

class SessionRefreshResponse:
    id_token: Optional[str]
    refresh_token: Optional[str]
    expires_in: Optional[str]
    token_type: Optional[str]
    message: Optional[str]
    error: Optional[str]

    def __init__(self, id_token: Optional[str] = None, refresh_token: Optional[str] = None,
                 expires_in: Optional[str] = None, token_type: Optional[str] = None,
                 message: Optional[str] = None, error: Optional[str] = None):
        self.id_token = id_token
        self.refresh_token = refresh_token
        self.expires_in = expires_in
        self.token_type = token_type
        self.message = message
        self.error = error

class PasswordResetRequest:
    email: str

    def __init__(self, email: str):
        self.email = email

class PasswordResetResponse:
    email: Optional[str]
    message: Optional[str]
    error: Optional[str]

    def __init__(self, email: Optional[str] = None, message: Optional[str] = None,
                 error: Optional[str] = None):
        self.email = email
        self.message = message
        self.error = error
