import json
from typing import Dict, Any, Optional

class SecretRequest:
    """Defines a generic request model for fetching secrets."""
    def __init__(self, secret_id: str, version_stage: Optional[str] = None):
        self.secret_id = secret_id
        self.version_stage = version_stage

    def to_dict(self) -> Dict[str, Any]:
        return {k: v for k, v in self.__dict__.items() if v is not None}

class SecretResponse:
    """Defines a generic response model for retrieved secrets."""
    def __init__(self, secret_value: Any, metadata: Optional[Dict[str, Any]] = None):
        self.secret_value = secret_value
        self.metadata = metadata if metadata is not None else {}

    def get_string_value(self) -> Optional[str]:
        if isinstance(self.secret_value, str):
            return self.secret_value
        return None

    def get_json_value(self) -> Optional[Dict[str, Any]]:
        if isinstance(self.secret_value, str):
            try:
                return json.loads(self.secret_value)
            except json.JSONDecodeError:
                pass
        elif isinstance(self.secret_value, dict):
            return self.secret_value
        return None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "secret_value": self.secret_value,
            "metadata": self.metadata
        }

