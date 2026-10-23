from dataclasses import dataclass
from typing import Optional

@dataclass
class SecretPayload:
    name: str
    data: str
    version: str

@dataclass
class SecretMetadata:
    name: str
    labels: Optional[dict] = None
    create_time: Optional[str] = None
    expire_time: Optional[str] = None
    version_count: Optional[int] = None

@dataclass
class RotationSummary:
    secret_id: str
    status: str
    last_rotated: Optional[str] = None
    next_rotation: Optional[str] = None

@dataclass
class AuditNote:
    secret_id: str
    note_id: str
    content: str
