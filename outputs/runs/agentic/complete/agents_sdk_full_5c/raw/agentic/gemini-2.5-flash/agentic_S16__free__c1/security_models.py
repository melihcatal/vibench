from dataclasses import dataclass, field
from typing import Optional, List

@dataclass
class SecretMetadata:
    secret_id: str
    name: str
    description: Optional[str] = None
    tags: Optional[dict] = field(default_factory=dict)
    created_time: Optional[str] = None
    last_rotated_time: Optional[str] = None
    next_rotation_time: Optional[str] = None
    rotation_enabled: bool = False

@dataclass
class SecretRotationSummary:
    secret_id: str
    status: str  # e.g., 'ROTATED', 'PENDING_ROTATION', 'NEVER_ROTATED'
    last_rotated_at: Optional[str] = None
    next_rotation_at: Optional[str] = None
    notes: Optional[str] = None

@dataclass
class SecretAuditNote:
    secret_id: str
    version_id: str
    note_content: str
    timestamp: str
    user_id: Optional[str] = None
    embedding: Optional[List[float]] = None # For semantic search
