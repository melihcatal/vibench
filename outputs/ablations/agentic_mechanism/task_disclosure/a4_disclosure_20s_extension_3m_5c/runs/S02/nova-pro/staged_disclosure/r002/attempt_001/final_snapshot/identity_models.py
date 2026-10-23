from typing import Any, Dict, Optional


class FederatedLoginRequest:
    def __init__(self, provider: str, code: str, state: Optional[str] = None):
        self.provider = provider
        self.code = code
        self.state = state

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "FederatedLoginRequest":
        return cls(
            provider=data.get("provider"),
            code=data.get("code"),
            state=data.get("state"),
        )


class FederatedLoginResponse:
    def __init__(self, success: bool, user_id: Optional[str] = None, error: Optional[str] = None):
        self.success = success
        self.user_id = user_id
        self.error = error

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "user_id": self.user_id,
            "error": self.error,
        }


def normalize_federated_login_response(response: Dict[str, Any]) -> FederatedLoginResponse:
    return FederatedLoginResponse(
        success=response.get("success", False),
        user_id=response.get("user_id"),
        error=response.get("error"),
    )