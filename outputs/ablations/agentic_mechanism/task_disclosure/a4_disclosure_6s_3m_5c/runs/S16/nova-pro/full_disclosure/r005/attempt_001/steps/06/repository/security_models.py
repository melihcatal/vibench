from typing import Any, Dict, List, Optional


class SecretRequest:
    def __init__(self, secret_id: str, version_id: Optional[str] = None):
        self.secret_id = secret_id
        self.version_id = version_id

    def to_dict(self) -> Dict[str, Any]:
        return {
            'secret_id': self.secret_id,
            'version_id': self.version_id
        }


class SecretResponse:
    def __init__(self, secret_id: str, version_id: str, secret_value: str):
        self.secret_id = secret_id
        self.version_id = version_id
        self.secret_value = secret_value

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'SecretResponse':
        return cls(
            secret_id=data['secret_id'],
            version_id=data['version_id'],
            secret_value=data['secret_value']
        )


def normalize_secret_response(response: Dict[str, Any]) -> SecretResponse:
    return SecretResponse.from_dict(response)