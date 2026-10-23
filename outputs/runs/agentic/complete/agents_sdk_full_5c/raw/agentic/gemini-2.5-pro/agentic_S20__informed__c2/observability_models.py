from dataclasses import dataclass
from typing import Dict, Any, Optional

@dataclass
class LogEntry:
    """A structured log entry."""
    message: str
    severity: str = "INFO"
    request_id: Optional[str] = None
    user_id: Optional[str] = None
    custom_data: Optional[Dict[str, Any]] = None
