from dataclasses import dataclass
from typing import Optional, Dict

@dataclass
class SecretValue:
    """Represents a fetched secret's value."""
    secret_id: str
    value: str
    version_id: str
    version_stage: Optional[list[str]] = None

@dataclass
class ParsedSecretValue:
    """Represents a fetched and parsed JSON secret."""
    secret_id: str
    value: Dict
    version_id: str

@dataclass
class RotationStatus:
    """Represents the status of a secret rotation."""
    secret_id: str
    enabled: bool
    last_rotated_date: Optional[str] = None
    next_rotation_date: Optional[str] = None
