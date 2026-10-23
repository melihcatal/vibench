from typing import Any, Dict, Optional

class EmailPasswordRequest:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

    def to_dict(self) -> Dict[str, Any]:
        return {"email": self.email, "password": self.password}

class EmailPasswordResponse:
    def __init__(self, access_token: Optional[str] = None, refresh_token: Optional[str] = None):
        self.access_token = access_token
        self.refresh_token = refresh_token

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(data.get("access_token"), data.get("refresh_token"))

class EmailPasswordNormalizer:
    @staticmethod
    def normalize_response(response: Dict[str, Any]) -> EmailPasswordResponse:
        return EmailPasswordResponse.from_dict(response)