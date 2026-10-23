from typing import Optional, Dict, Any

class SecretPayload:
    secret_id: str
    version_id: Optional[str] = None
    version_stage: Optional[str] = None
    key_field: Optional[str] = None

    def __init__(self, secret_id: str, version_id: Optional[str] = None, version_stage: Optional[str] = None, key_field: Optional[str] = None):
        self.secret_id = secret_id
        self.version_id = version_id
        self.version_stage = version_stage
        self.key_field = key_field

class SecretResponse:
    secret_value: Any
    metadata: Dict[str, Any]

    def __init__(self, secret_value: Any, metadata: Dict[str, Any]):
        self.secret_value = secret_value
        self.metadata = metadata
