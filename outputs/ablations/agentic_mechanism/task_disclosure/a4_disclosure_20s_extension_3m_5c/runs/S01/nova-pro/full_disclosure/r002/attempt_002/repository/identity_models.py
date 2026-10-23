from typing import Any, Dict, Optional

class EmailPasswordRequest:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

class EmailPasswordResponse:
    def __init__(self, success: bool, message: Optional[str] = None, tokens: Optional[Dict[str, Any]] = None):
        self.success = success
        self.message = message
        self.tokens = tokens if tokens else {}

def normalize_response(response: Dict[str, Any]) -> EmailPasswordResponse:
    success = response.get('success', False)
    message = response.get('message', None)
    tokens = response.get('tokens', {})
    return EmailPasswordResponse(success, message, tokens)