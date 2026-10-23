from typing import Any, Dict

# Simple JSON validation model for secret payloads

class SecretPayloadModel:
    def __init__(self, data: Dict[str, Any]):
        self.raw = data
        self.validate()

    def validate(self) -> None:
        """Basic schema validation for secrets that should contain
        username, password, and host fields for DB connections.
        """
        required = {'username', 'password', 'host'}
        if not required.issubset(self.raw.keys()):
            raise ValueError(f"Secret payload missing required fields: {required - set(self.raw.keys())}")

    def to_dict(self) -> Dict[str, Any]:
        return self.raw

# Example usage:
# payload = SecretPayloadModel(json.loads(secret_json))
