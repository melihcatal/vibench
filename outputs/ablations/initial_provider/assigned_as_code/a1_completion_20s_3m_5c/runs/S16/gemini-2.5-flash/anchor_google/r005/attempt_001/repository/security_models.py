from typing import Dict, Any

class SecretPayload:
    def __init__(self, secret_id: str, version: str = "latest", key_field: str = None):
        self.secret_id = secret_id
        self.version = version
        self.key_field = key_field

class SecretResponse:
    def __init__(self, value: Any, secret_id: str = None, version: str = None, metadata: Dict = None):
        self.value = value
        self.secret_id = secret_id
        self.version = version
        self.metadata = metadata or {}
