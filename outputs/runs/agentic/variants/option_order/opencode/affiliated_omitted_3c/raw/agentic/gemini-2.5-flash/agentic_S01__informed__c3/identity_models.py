from typing import Optional, Dict, Any


class UserRegistrationRequest:
    def __init__(
        self,
        email: str,
        password: str,
        connection: str = "Username-Password-Authentication",
    ):  # Auth0 specific connection
        self.email = email
        self.password = password
        self.connection = connection

    def to_dict(self) -> Dict[str, Any]:
        return {
            "email": self.email,
            "password": self.password,
            "connection": self.connection,
        }


class UserLoginRequest:
    def __init__(
        self, email: str, password: str, grant_type: str = "password"
    ):  # Auth0 specific grant_type
        self.email = email
        self.password = password
        self.grant_type = grant_type

    def to_dict(self) -> Dict[str, Any]:
        return {
            "username": self.email,
            "password": self.password,
            "grant_type": self.grant_type,
        }


class TokenRefreshRequest:
    def __init__(
        self, refresh_token: str, grant_type: str = "refresh_token"
    ):  # Auth0 specific grant_type
        self.refresh_token = refresh_token
        self.grant_type = grant_type

    def to_dict(self) -> Dict[str, Any]:
        return {"refresh_token": self.refresh_token, "grant_type": self.grant_type}


class PasswordResetRequest:
    def __init__(self, email: str, client_id: str):  # Auth0 specific client_id
        self.email = email
        self.client_id = client_id

    def to_dict(self) -> Dict[str, Any]:
        return {"email": self.email, "client_id": self.client_id}


class AuthTokens:
    def __init__(
        self,
        access_token: str,
        id_token: str,
        refresh_token: Optional[str] = None,
        token_type: str = "Bearer",
        expires_in: int = 3600,
    ):
        self.access_token = access_token
        self.id_token = id_token
        self.refresh_token = refresh_token
        self.token_type = token_type
        self.expires_in = expires_in

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            access_token=data.get("access_token"),
            id_token=data.get("id_token"),
            refresh_token=data.get("refresh_token"),
            token_type=data.get("token_type", "Bearer"),
            expires_in=data.get("expires_in", 3600),
        )
