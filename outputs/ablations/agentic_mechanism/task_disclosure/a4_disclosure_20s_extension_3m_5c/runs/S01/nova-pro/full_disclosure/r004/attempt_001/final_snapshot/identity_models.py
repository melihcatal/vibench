from typing import Any, Dict, Optional


class EmailPasswordRequest:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password


class EmailPasswordResponse:
    def __init__(self, success: bool, message: Optional[str] = None):
        self.success = success
        self.message = message


def normalize_email_password_response(response: Dict[str, Any]) -> EmailPasswordResponse:
    success = response.get('success', False)
    message = response.get('message', None)
    return EmailPasswordResponse(success=success, message=message)