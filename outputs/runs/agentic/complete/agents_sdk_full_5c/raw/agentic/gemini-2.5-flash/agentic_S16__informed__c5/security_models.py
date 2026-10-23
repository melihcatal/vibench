import json
from typing import Any, Dict, Optional

class Secret:
    """Base class for representing a secret."""
    def __init__(self, name: str, value: Any, version: Optional[str] = None):
        self.name = name
        self.value = value
        self.version = version

    def to_dict(self) -> Dict[str, Any]:
        return {"name": self.name, "value": self.value, "version": self.version}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(name=data["name"], value=data["value"], version=data.get("version"))

def parse_secret_string_as_json(secret_string: str) -> Dict[str, Any]:
    """Parses a secret string expected to be in JSON format."""
    try:
        return json.loads(secret_string)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to decode JSON secret string: {e}")

