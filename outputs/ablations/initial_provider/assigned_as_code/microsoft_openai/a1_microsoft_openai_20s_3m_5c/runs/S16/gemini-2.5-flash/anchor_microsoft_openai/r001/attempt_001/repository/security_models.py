from dataclasses import dataclass, field
from typing import Dict, Optional

@dataclass
class SecretInfo:
    name: str
    value: str
    version_id: Optional[str] = None
    content_type: Optional[str] = None
    tags: Optional[Dict[str, str]] = field(default_factory=dict)
    enabled: Optional[bool] = None
    expires_on: Optional[str] = None
    created_on: Optional[str] = None
    updated_on: Optional[str] = None

@dataclass
class RotationStatus:
    secret_id: str
    last_rotated: Optional[str] = None
    next_rotation_due: Optional[str] = None
    status: Optional[str] = None # e.g., 'rotated', 'pending_rotation', 'failed'
