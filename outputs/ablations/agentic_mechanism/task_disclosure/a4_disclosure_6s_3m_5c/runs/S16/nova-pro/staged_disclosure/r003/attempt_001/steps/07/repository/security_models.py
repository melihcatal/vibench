from typing import Any, Dict


class SecretRequest:
    def __init__(self, secret_name: str):
        self.secret_name = secret_name

    def to_dict(self) -> Dict[str, Any]:
        return {'secret_name': self.secret_name}


class SecretResponse:
    def __init__(self, secret_value: str):
        self.secret_value = secret_value

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SecretResponse':
        return cls(secret_value=data['secret_value'])


def normalize_secret_response(response: Dict[str, Any]) -> SecretResponse:
    return SecretResponse.from_dict(response)