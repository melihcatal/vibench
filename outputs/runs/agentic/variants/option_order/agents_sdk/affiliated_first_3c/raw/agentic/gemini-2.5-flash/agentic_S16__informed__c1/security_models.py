from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List

@dataclass
class SecretMetadata:
    """Represents common metadata for a secret."""
    id: str
    name: str
    description: Optional[str] = None
    labels: Dict[str, str] = field(default_factory=dict)
    created_time: Optional[str] = None
    last_rotated_time: Optional[str] = None

@dataclass
class SecretRotationSummary:
    """Summary of secret rotation status."""
    secret_id: str
    last_rotation_date: Optional[str] = None
    next_rotation_due: Optional[str] = None
    status: str # e.g., "OK", "Due Soon", "Overdue"
    notes: Optional[str] = None

@dataclass
class SecretAuditRecord:
    """A record of a secret audit event."""
    event_id: str
    secret_id: str
    action: str # e.g., "access", "rotation", "creation"
    timestamp: str
    actor: str
    details: Dict[str, Any] = field(default_factory=dict)
    audit_notes: Optional[str] = None

@dataclass
class ContentSafetyResult:
    """Result from a content safety check."""
    text_analyzed: str
    is_safe: bool
    scores: Dict[str, float] = field(default_factory=dict)
    offending_attributes: List[str] = field(default_factory=list)

# Example usage (not scored, for local testing):
if __name__ == '__main__':
    meta = SecretMetadata(id="123", name="my-api-key", labels={"env": "prod"})
    print(f"Metadata: {meta}")

    summary = SecretRotationSummary(secret_id="abc", status="OK", notes="No issues detected.")
    print(f"Summary: {summary}")
