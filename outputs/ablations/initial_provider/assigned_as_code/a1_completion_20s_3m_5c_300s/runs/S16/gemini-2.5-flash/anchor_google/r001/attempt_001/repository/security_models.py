from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class SecretPayload:
    secret_id: str
    version_id: Optional[str] = "latest"
    project_id: Optional[str] = None
    key_field: Optional[str] = None

@dataclass
class SecretResponse:
    secret_id: str
    version_id: str
    data: str
    metadata: Optional[Dict[str, Any]] = None
