from typing import List, Dict, Any

class RegisterRequest:
    def __init__(self, username: str, password: str, user_attributes: List[Dict[str, str]], **custom_attrs):
        self.username = username
        self.password = password
        self.user_attributes = user_attributes
        self.custom_attrs = custom_attrs

class RegisterResponse:
    def __init__(self, username: str, user_status: str, user_create_date: str, enabled: bool, user_attributes: List[Dict[str, str]], **extra):
        self.username = username
        self.user_status = user_status
        self.user_create_date = user_create_date
        self.enabled = enabled
        self.user_attributes = user_attributes
        self.extra = extra

class LoginRequest:
    def __init__(self, username: str, password: str):
        self.auth_flow = 'USER_PASSWORD_AUTH'
        self.client_id = None  # placeholder for client id if needed
        self.auth_parameters = {'USERNAME': username, 'PASSWORD': password}

class LoginResponse:
    def __init__(self, access_token: str, id_token: str, refresh_token: str, expires_in: int, token_type: str, **extra):
        self.access_token = access_token
        self.id_token = id_token
        self.refresh_token = refresh_token
        self.expires_in = expires_in
        self.token_type = token_type
        self.extra = extra

class RefreshTokenRequest:
    def __init__(self, refresh_token: str):
        self.refresh_token = refresh_token

class RefreshTokenResponse:
    def __init__(self, access_token: str, id_token: str, expires_in: int, token_type: str, **extra):
        self.access_token = access_token
        self.id_token = id_token
        self.expires_in = expires_in
        self.token_type = token_type
        self.extra = extra

class ForgotPasswordRequest:
    def __init__(self, username: str):
        self.username = username

class ForgotPasswordSubmitRequest:
    def __init__(self, username: str, confirmation_code: str, password: str):
        self.username = username
        self.confirmation_code = confirmation_code
        self.password = password

class PasswordResetResponse:
    def __init__(self, status: str = 'SUCCESS'):
        self.status = status
