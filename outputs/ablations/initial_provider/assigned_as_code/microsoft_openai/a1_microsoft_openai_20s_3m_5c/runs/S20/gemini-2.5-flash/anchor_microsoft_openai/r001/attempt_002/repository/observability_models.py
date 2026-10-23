from typing import Any, Dict, List, Optional
from datetime import datetime, timezone

class LogEntry:
    def __init__(self, message: str, severity: str = "INFO", timestamp: Optional[datetime] = None, **kwargs):
        self.message = message
        self.severity = severity
        self.timestamp = timestamp if timestamp else datetime.now(timezone.utc)
        self.properties = kwargs

    def to_azure_monitor_format(self) -> Dict[str, Any]:
        log_data = {
            "TimeGenerated": self.timestamp.isoformat(),
            "message": self.message,
            "severity": self.severity,
        }
        log_data.update(self.properties)
        return log_data

class QueryResults:
    def __init__(self, logs: List[LogEntry], next_link: Optional[str] = None):
        self.logs = logs
        self.next_link = next_link
