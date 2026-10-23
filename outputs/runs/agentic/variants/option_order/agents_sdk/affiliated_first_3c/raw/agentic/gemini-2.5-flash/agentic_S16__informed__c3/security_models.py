import json
from typing import Dict, Any, Optional

class SecretValue:
    """Represents a secret value."""
    def __init__(self, name: str, value: str, version: str = "latest"):
        self.name = name
        self.value = value
        self.version = version

    def to_dict(self) -> Dict[str, Any]:
        return {"name": self.name, "value": self.value, "version": self.version}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(name=data["name"], value=data["value"], version=data.get("version", "latest"))

class JsonSecret:
    """Represents a JSON-formatted secret."""
    def __init__(self, name: str, json_data: Dict[str, Any], version: str = "latest"):
        self.name = name
        self.json_data = json_data
        self.version = version

    def get_value(self, key: str) -> Optional[Any]:
        return self.json_data.get(key)

    def to_dict(self) -> Dict[str, Any]:
        return {"name": self.name, "json_data": self.json_data, "version": self.version}

    @classmethod
    def from_string(cls, name: str, json_string: str, version: str = "latest"):
        try:
            json_data = json.loads(json_string)
            return cls(name=name, json_data=json_data, version=version)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON string provided for secret.")
