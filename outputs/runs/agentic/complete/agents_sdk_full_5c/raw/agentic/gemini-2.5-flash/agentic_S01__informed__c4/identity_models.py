from typing import Optional, Dict, Any

class UserRegistrationRequest:
    def __init__(self, email: str, password: str, display_name: Optional[str] = None):
        self.email = email
        self.password = password
        self.display_name = display_name

    def to_dict(self) -> Dict[str, Any]:
        data = {"email": self.email, "password": self.password}
        if self.display_name:
            data["displayName"] = self.display_name
        return data

class UserLoginRequest:
    def __init__(self, id_token: str):
        self.id_token = id_token

    def to_dict(self) -> Dict[str, Any]:
        return {"idToken": self.id_token}

class PasswordResetRequest:
    def __init__(self, email: str):
        self.email = email

    def to_dict(self) -> Dict[str, Any]:
        return {"email": self.email}

class AuthResponse:
    def __init__(self, uid: str, email: str, message: str, token: Optional[str] = None):
        self.uid = uid
        self.email = email
        self.message = message
        self.token = token

    def to_dict(self) -> Dict[str, Any]:
        data = {"uid": self.uid, "email": self.email, "message": self.message}
        if self.token:
            data["token"] = self.token
        return data

class ErrorResponse:
    def __init__(self, error: str):
        self.error = error

    def to_dict(self) -> Dict[str, Any]:
        return {"error": self.error}
