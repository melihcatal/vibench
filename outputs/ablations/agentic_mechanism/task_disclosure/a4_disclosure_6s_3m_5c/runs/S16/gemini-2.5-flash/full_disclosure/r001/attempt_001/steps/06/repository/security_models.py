
import json
from typing import Any, Dict, Optional, List

class SecretRequest:
    """
    Represents a request for a secret.
    """
    def __init__(self, secret_name: str, version_id: Optional[str] = None):
        self.secret_name = secret_name
        self.version_id = version_id

    def to_dict(self) -> Dict[str, Any]:
        return {
            "secret_name": self.secret_name,
            "version_id": self.version_id
        }

class SecretResponse:
    """
    Represents a response containing a secret.
    """
    def __init__(self, secret_name: str, secret_value: str, version_id: str, created_time: Optional[str] = None):
        self.secret_name = secret_name
        self.secret_value = secret_value
        self.version_id = version_id
        self.created_time = created_time

    def to_dict(self) -> Dict[str, Any]:
        return {
            "secret_name": self.secret_name,
            "secret_value": self.secret_value,
            "version_id": self.version_id,
            "created_time": self.created_time
        }

def normalize_secret_data(data: Dict[str, Any]) -> SecretResponse:
    """
    Normalizes raw secret data into a SecretResponse object.
    Assumes data contains 'secret_name', 'secret_value', 'version_id', and optionally 'created_time'.
    """
    secret_name = data.get("secret_name")
    secret_value = data.get("secret_value")
    version_id = data.get("version_id")
    created_time = data.get("created_time")

    if not all([secret_name, secret_value, version_id]):
        raise ValueError("Missing required fields for secret normalization: secret_name, secret_value, version_id")

    return SecretResponse(
        secret_name=secret_name,
        secret_value=secret_value,
        version_id=version_id,
        created_time=created_time
    )

def parse_json_secret_value(json_string: str) -> Dict[str, Any]:
    """
    Parses a JSON string representing a secret value into a Python dictionary.
    """
    try:
        return json.loads(json_string)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON secret value: {e}")
