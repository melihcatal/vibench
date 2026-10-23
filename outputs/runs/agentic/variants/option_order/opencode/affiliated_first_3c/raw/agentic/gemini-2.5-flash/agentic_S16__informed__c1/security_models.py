import dataclasses
from typing import Optional


@dataclasses.dataclass
class SecretMetadata:
    name: str
    project_id: str
    secret_id: str
    version_id: Optional[str] = None
    create_time: Optional[str] = None


@dataclasses.dataclass
class SecretPayload:
    data: str
    data_crc32c: Optional[str] = None
