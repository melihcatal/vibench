"""
This file contains local data models for observability.
"""
from dataclasses import dataclass
from typing import Any, Dict, Optional

@dataclass
class StructuredLog:
    """A simple data class for a structured log entry."""
    message: str
    severity: str
    request_id: Optional[str] = None
    user_id: Optional[str] = None
    extra_data: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Converts the log entry to a dictionary for JSON serialization."""
        log_dict = {
            "message": self.message,
            "severity": self.severity,
        }
        if self.request_id:
            log_dict["request_id"] = self.request_id
        if self.user_id:
            log_dict["user_id"] = self.user_id
        if self.extra_data:
            log_dict.update(self.extra_data)
        return log_dict
