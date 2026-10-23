from typing import Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class Secret:
    name: str
    value: Any
    provider: str
    version: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

@dataclass
class SecretRotationStatus:
    secret_name: str
    last_rotated: Optional[str] = None
    next_rotation_due: Optional[str] = None
    status: str # e.g., "healthy", "due_soon", "overdue"
    provider: str

@dataclass
class SecretAuditEntry:
    secret_name: str
    action: str # e.g., "accessed", "rotated", "deleted"
    timestamp: str
    actor: str
    details: Optional[Dict[str, Any]] = None

