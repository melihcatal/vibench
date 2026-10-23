from typing import Any, Dict, Union


class FederatedLoginRequest:
    def __init__(self, provider: str, access_token: str):
        self.provider = provider
        self.access_token = access_token

    def to_dict(self) -> Dict[str, Any]:
        return {
            'provider': self.provider,
            'access_token': self.access_token,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FederatedLoginRequest':
        return cls(
            provider=data['provider'],
            access_token=data['access_token'],
        )


class FederatedLoginResponse:
    def __init__(self, user_id: str, email: str, name: str):
        self.user_id = user_id
        self.email = email
        self.name = name

    def to_dict(self) -> Dict[str, Any]:
        return {
            'user_id': self.user_id,
            'email': self.email,
            'name': self.name,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FederatedLoginResponse':
        return cls(
            user_id=data['user_id'],
            email=data['email'],
            name=data['name'],
        )


def normalize_federated_login_response(response: Dict[str, Any]) -> FederatedLoginResponse:
    return FederatedLoginResponse.from_dict(response)