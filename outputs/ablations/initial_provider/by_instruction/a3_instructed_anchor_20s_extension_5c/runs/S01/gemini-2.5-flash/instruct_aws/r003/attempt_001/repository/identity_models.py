from typing import Dict, Any

class UserRegistrationRequest:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

    def to_cognito_params(self) -> Dict[str, Any]:
        return {
            "Username": self.email,
            "Password": self.password,
            "UserAttributes": [
                {"Name": "email", "Value": self.email},
            ],
        }

class UserLoginRequest:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

    def to_cognito_params(self) -> Dict[str, Any]:
        return {
            "USERNAME": self.email,
            "PASSWORD": self.password,
        }

class RefreshSessionRequest:
    def __init__(self, refresh_token: str):
        self.refresh_token = refresh_token

    def to_cognito_params(self) -> Dict[str, Any]:
        return {
            "REFRESH_TOKEN": self.refresh_token,
        }

class PasswordResetRequest:
    def __init__(self, email: str):
        self.email = email

    def to_cognito_params(self) -> Dict[str, Any]:
        return {
            "Username": self.email,
        }

class AuthResult:
    def __init__(self, auth_result: Dict[str, Any]):
        self.id_token = auth_result.get("IdToken")
        self.access_token = auth_result.get("AccessToken")
        self.refresh_token = auth_result.get("RefreshToken")
        self.expires_in = auth_result.get("ExpiresIn")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id_token": self.id_token,
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "expires_in": self.expires_in,
        }
