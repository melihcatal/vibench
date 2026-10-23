from typing import Dict, Any, Optional

class UserCreateRequest:
    def __init__(self, email: str, password: str, connection: str = 'Username-Password-Authentication', email_verified: bool = False):
        self.email = email
        self.password = password
        self.connection = connection
        self.email_verified = email_verified

class UserCreateResponse:
    def __init__(self, user_id: str, email: str, created_at: str):
        self.user_id = user_id
        self.email = email
        self.created_at = created_at

class PasswordResetTicket:
    def __init__(self, ticket_id: str, ticket_url: str):
        self.ticket_id = ticket_id
        self.ticket_url = ticket_url

class PasswordResetResponse:
    def __init__(self, success: bool):
        self.success = success

class TokenRefreshRequest:
    def __init__(self, refresh_token: str):
        self.refresh_token = refresh_token

class TokenRefreshResponse:
    def __init__(self, access_token: str, refresh_token: Optional[str] = None):
        self.access_token = access_token
        self.refresh_token = refresh_token

class TokenResponse:
    def __init__(self, access_token: str, id_token: str):
        self.access_token = access_token
        self.id_token = id_token
