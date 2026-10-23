import json
from typing import Any, Dict, Optional

class SecretPayload:
    """
    A simple model to represent a secret's payload, handling both string and JSON.
    """
    def __init__(self, value: str):
        self._raw_value = value
        self._json_value = None
        try:
            self._json_value = json.loads(value)
        except json.JSONDecodeError:
            pass # Not a JSON string

    @property
    def raw(self) -> str:
        """
        Returns the raw string value of the secret.
        """
        return self._raw_value

    @property
    def json(self) -> Optional[Dict[str, Any]]:
        """
        Returns the parsed JSON dictionary if the secret is valid JSON, otherwise None.
        """
        return self._json_value

    def is_json(self) -> bool:
        """
        Checks if the secret payload is a valid JSON string.
        """
        return self._json_value is not None

    def __str__(self):
        return self._raw_value

    def __repr__(self):
        return f"SecretPayload(raw='{self._raw_value[:50]}...')"

class SecretMetadata:
    """
    A simple model to represent common secret metadata.
    """
    def __init__(self, name: str, version: Optional[str] = None, 
                 created_time: Optional[str] = None, 
                 last_accessed_time: Optional[str] = None,
                 labels: Optional[Dict[str, str]] = None):
        self.name = name
        self.version = version
        self.created_time = created_time
        self.last_accessed_time = last_accessed_time
        self.labels = labels if labels is not None else {}
    
    def __repr__(self):
        return f"SecretMetadata(name='{self.name}', version='{self.version}', labels={self.labels})"
