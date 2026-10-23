from pydantic import BaseModel
from typing import Dict, Any, Optional


class StructuredLogEvent(BaseModel):
    """Model for structured log events sent to Datadog."""

    timestamp: str
    severity: str
    source: str
    message: str
    attributes: Dict[str, Any]
    service: str
    hostname: str

    def dict(self, **kwargs) -> Dict[str, Any]:
        """Convert model to dict for serialization."""
        base_dict = super().dict(**kwargs)
        base_dict.update(self.attributes)
        return base_dict


def normalize_log_response(log_entry: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize Datadog log query responses."""
    return {
        "timestamp": log_entry.get("timestamp"),
        "severity": log_entry.get("status"),
        "message": log_entry.get("message"),
        "attributes": {
            k: v
            for k, v in log_entry.items()
            if k not in ["timestamp", "status", "message"]
        },
        "service": log_entry.get("service"),
        "hostname": log_entry.get("host"),
    }
