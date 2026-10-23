from typing import Dict, Optional

# Simple request/response dataclasses for email/password flows

class RegisterRequest:
    def __init__(self, email: str, password: str, connection: str = 'Username-Password-Authentication',
                 user_metadata: Optional[Dict]=None):
        self.email = email
        self.password = password
        self.connection = connection
        self.user_metadata = user_metadata or {}

    def to_dict(self) -> Dict:
        return {
            'email': self.email,
            'password': self.password,
            'connection': self.connection,
            'user_metadata': self.user_metadata
        }

# -------- Login --------
class LoginRequest:
    def __init__(self, client_id: str, username: str, password: str, grant_type: str = 'password',
                 audience: str = 'https://{domain}/api/v2/', scope: str = 'openid profile email'):
        self.client_id = client_id
        self.username = username
        self.password = password
        self.grant_type = grant_type
        self.audience = audience
        self.scope = scope

    def to_dict(self) -> Dict:
        return {
            'client_id': self.client_id,
            'username': self.username,
            'password': self.password,
            'grant_type': self.grant_type,
            'audience': self.audience,
            'scope': self.scope
        }

class LoginResponse:
    def __init__(self, id_token: str, access_token: str, refresh_token: str, expires_in: int):
        self.id_token = id_token
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expires_in = expires_in

# -------- Refresh --------
class RefreshRequest:
    def __init__(self, refresh_token: str):
        self.refresh_token = refresh_token

    def to_dict(self) -> Dict:
        return {'refresh_token': self.refresh_token}

class RefreshResponse:
    def __init__(self, access_token: str, expires_in: int):
        self.access_token = access_token
        self.expires_in = expires_in

# -------- Reset --------
class ResetPasswordRequest:
    def __init__(self, email: str, connection: str):
        self.email = email
        self.connection = connection

    def to_dict(self) -> Dict:
        return {'email': self.email, 'connection': self.connection}
