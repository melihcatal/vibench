from dataclasses import dataclass
from typing import Any, Dict, Optional

@dataclass
class LogEvent:
    timestamp: int  # Unix timestamp in milliseconds
    message: str

@dataclass
class StructuredLogMessage:
    level: str
    service: str
    event: str
    timestamp: float # Unix timestamp in seconds
    correlation_id: Optional[str] = None
    user_id: Optional[str] = None
    ip_address: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
