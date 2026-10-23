import json
from typing import Dict, Any, Optional

class SecretMetadata:
    """
    A simple model to represent secret metadata.
    """
    def __init__(self, secret_id: str, labels: Optional[Dict[str, str]] = None, description: Optional[str] = None):
        self.secret_id = secret_id
        self.labels = labels if labels is not None else {}
        self.description = description

    def to_dict(self) -> Dict[str, Any]:
        return {
            "secret_id": self.secret_id,
            "labels": self.labels,
            "description": self.description
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            secret_id=data.get("secret_id"),
            labels=data.get("labels"),
            description=data.get("description")
        )

class JSONSecret:
    """
    A model for parsed JSON secrets.
    """
    def __init__(self, data: Dict[str, Any]):
        self._data = data

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def to_dict(self) -> Dict[str, Any]:
        return self._data

    @classmethod
    def from_json_string(cls, json_string: str):
        return cls(json.loads(json_string))

if __name__ == "__main__":
    # Example usage for SecretMetadata
    metadata = SecretMetadata(
        secret_id="my-app-secret",
        labels={"env": "prod", "owner": "devteam"},
        description="API key for my application"
    )
    print(f"SecretMetadata dict: {metadata.to_dict()}")

    # Example usage for JSONSecret
    json_str = '''{"username": "testuser", "password": "securepassword"}'''
    json_secret = JSONSecret.from_json_string(json_str)
    print(f"JSONSecret username: {json_secret.get('username')}")
