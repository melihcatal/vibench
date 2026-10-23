from typing import Dict, Any


class SecretPayload:
    """Represents a secret payload."""

    def __init__(self, data: str):
        self.data = data

    def to_json(self) -> Dict[str, Any]:
        """Converts the secret data to a JSON object if possible."""
        try:
            import json

            return json.loads(self.data)
        except json.JSONDecodeError:
            return {"raw_data": self.data}
