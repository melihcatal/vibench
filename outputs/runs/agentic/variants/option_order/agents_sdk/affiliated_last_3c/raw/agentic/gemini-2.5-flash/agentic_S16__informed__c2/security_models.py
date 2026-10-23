from dataclasses import dataclass
from typing import Optional

@dataclass
class SecretPayload:
    name: str
    value: str
    version: Optional[str] = None
    created_time: Optional[str] = None

@dataclass
class SecretMetadata:
    secret_id: str
    project_id: str
    labels: Optional[dict] = None
    annotations: Optional[dict] = None
    replication_status: Optional[str] = None
