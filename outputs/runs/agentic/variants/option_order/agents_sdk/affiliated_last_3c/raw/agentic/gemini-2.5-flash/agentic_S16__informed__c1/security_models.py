from dataclasses import dataclass, field
from typing import Optional, Dict, Any

@dataclass
class SecretMetadata:
    id: str
    name: str
    description: Optional[str] = None
    labels: Dict[str, str] = field(default_factory=dict)
    created_time: Optional[str] = None
    updated_time: Optional[str] = None

@dataclass
class SecretVersion:
    id: str
    secret_id: str
    created_time: Optional[str] = None
    state: Optional[str] = None # e.g., ENABLED, DISABLED
    payload_checksum: Optional[str] = None

@dataclass
class ParsedJsonSecret:
    secret_id: str
    data: Dict[str, Any]

@dataclass
class SecretRotationSummary:
    secret_id: str
    last_rotated: Optional[str] = None
    next_rotation_due: Optional[str] = None
    status: str # e.g., "Healthy", "Overdue", "Warning"
    notes: Optional[str] = None

