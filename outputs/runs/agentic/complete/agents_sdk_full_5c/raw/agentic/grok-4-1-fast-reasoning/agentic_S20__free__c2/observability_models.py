from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, Any, Optional, List

@dataclass
class StructuredLogEvent:
    message: str
    severity: str = "INFO"
    service: str = field(default_factory=str)
    correlation_id: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    timestamp: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        d = {
            "message": self.message,
            "severity": self.severity,
            "service": self.service or "unknown",
        }
        if self.correlation_id:
            d["correlation_id"] = self.correlation_id
        if self.metadata:
            d.update(self.metadata)
        if self.timestamp:
            d["timestamp"] = self.timestamp.isoformat() + "Z"
        return d

@dataclass
class LogQuery:
    filter_str: str
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    page_size: int = 100

    def build_filter(self) -> str:
        f = self.filter_str
        if self.start_time:
            f += f' AND timestamp >= "{self.start_time.isoformat()}Z"'
        if self.end_time:
            f += f' AND timestamp <= "{self.end_time.isoformat()}Z"'
        return f
