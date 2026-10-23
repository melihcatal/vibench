from typing import Any, Dict, Union


class FederatedLoginRequest:
    def __init__(self, provider: str, user_id: str, access_token: str):
        self.provider = provider
        self.user_id = user_id
        self.access_token = access_token

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "FederatedLoginRequest":
        return FederatedLoginRequest(
            provider=data['provider'],
            user_id=data['user_id'],
            access_token=data['access_token']
        )


class FederatedLoginResponse:
    def __init__(self, success: bool, user_id: Union[str, None] = None, error: Union[str, None] = None):
        self.success = success
        self.user_id = user_id
        self.error = error

    def to_dict(self) -> Dict[str, Any]:
        return {
            'success': self.success,
            'user_id': self.user_id,
            'error': self.error
        }


def normalize_user_id(user_id: str) -> str:
    return user_id.lower().strip()
