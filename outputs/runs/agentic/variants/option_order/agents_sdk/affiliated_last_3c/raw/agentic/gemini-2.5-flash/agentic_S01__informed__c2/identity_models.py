from typing import Optional, Dict

class UserRegistrationRequest:
    def __init__(self, email: str, password: str, connection: str = "Username-Password-Authentication"):
        self.email = email
        self.password = password
        self.connection = connection

    def to_dict(self):
        return {
            "email": self.email,
            "password": self.password,
            "connection": self.connection
        }

class UserLoginRequest:
    def __init__(self, email: str, password: str, grant_type: str = "password", scope: str = "openid profile email offline_access"):
        self.email = email
        self.password = password
        self.grant_type = grant_type
        self.scope = scope
        self.client_id: Optional[str] = None # Will be set by client
        self.client_secret: Optional[str] = None # Will be set by client

    def to_dict(self):
        return {
            "username": self.email,
            "password": self.password,
            "grant_type": self.grant_type,
            "scope": self.scope,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }

class TokenRefreshRequest:
    def __init__(self, refresh_token: str, grant_type: str = "refresh_token"):
        self.refresh_token = refresh_token
        self.grant_type = grant_type
        self.client_id: Optional[str] = None # Will be set by client
        self.client_secret: Optional[str] = None # Will be set by client

    def to_dict(self):
        return {
            "grant_type": self.grant_type,
            "refresh_token": self.refresh_token,
            "client_id": self.client_id,
            "client_secret": self.client_secret
        }

class PasswordResetRequest:
    def __init__(self, email: str, connection: str = "Username-Password-Authentication"):
        self.email = email
        self.connection = connection
        self.client_id: Optional[str] = None # Will be set by client

    def to_dict(self):
        return {
            "email": self.email,
            "connection": self.connection,
            "client_id": self.client_id
        }

class AuthResponse:
    def __init__(self, response_data: Dict):
        self.access_token = response_data.get("access_token")
        self.id_token = response_data.get("id_token")
        self.refresh_token = response_data.get("refresh_token")
        self.expires_in = response_data.get("expires_in")
        self.token_type = response_data.get("token_type")

    def to_dict(self):
        return {
            "access_token": self.access_token,
            "id_token": self.id_token,
            "refresh_token": self.refresh_token,
            "expires_in": self.expires_in,
            "token_type": self.token_type
        }

class UserRegistrationResponse:
    def __init__(self, response_data: Dict):
        self.email = response_data.get("email")
        self.user_id = response_data.get("user_id")
        self.created_at = response_data.get("created_at")

    def to_dict(self):
        return {
            "email": self.email,
            "user_id": self.user_id,
            "created_at": self.created_at
        }
