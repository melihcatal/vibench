from typing import Any, Dict, Optional

class EmailPasswordRequest:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

    def to_dict(self) -> Dict[str, Any]:
        return {"email": self.email, "password": self.password}


class EmailPasswordResponse:
    def __init__(self, access_token: str, refresh_token: str):
        self.access_token = access_token
        self.refresh_token = refresh_token

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "EmailPasswordResponse":
        return cls(data["access_token"], data["refresh_token"])


def normalize_email_password_response(response: Dict[str, Any]) -> EmailPasswordResponse:
    return EmailPasswordResponse.from_dict(response)