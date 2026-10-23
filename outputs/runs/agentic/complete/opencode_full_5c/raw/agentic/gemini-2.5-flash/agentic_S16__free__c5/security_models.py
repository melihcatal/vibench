import dataclasses
from typing import Optional, Dict


@dataclasses.dataclass
class SecretPayload:
    name: str
    data: bytes
    version: str


@dataclasses.dataclass
class SecretMetadata:
    name: str
    project_id: str
    secret_id: str
    labels: Dict[str, str]
    annotations: Dict[str, str]
    create_time: str
    destroy_time: Optional[str] = None
    state: str
