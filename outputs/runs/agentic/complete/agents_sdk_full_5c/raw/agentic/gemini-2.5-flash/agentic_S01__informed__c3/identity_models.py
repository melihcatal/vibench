from typing import Optional

class UserRegisterRequest:
    def __init__(self, email: str, password: str, display_name: Optional[str] = None):
        self.email = email
        self.password = password
        self.display_name = display_name

class UserLoginRequest:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

class UserAuthResponse:
    def __init__(self, id_token: str, refresh_token: str, expires_in: str, email: str, local_id: str):
        self.id_token = id_token
        self.refresh_token = refresh_token
        self.expires_in = expires_in
        self.email = email
        self.local_id = local_id

class PasswordResetRequest:
    def __init__(self, email: str):
        self.email = email
