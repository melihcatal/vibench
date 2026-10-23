"""Local request, response, and normalization helpers for Managed Log Query / Log Ingestion."""

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, List, Optional, Union


@dataclass
class LogEntry:
    timestamp: datetime
    severity: str
    message: str
    service: str
    correlation_id: Optional[str] = None
    custom_fields: Optional[Dict[str, Union[str, int, float, bool]]] = None

    def to_dict(self) -> Dict:
        """Convert LogEntry to a dictionary for serialization."""
        data = asdict(self)
        data["timestamp"] = self.timestamp.isoformat()
        if self.custom_fields:
            data.update(self.custom_fields)
        return data


@dataclass
class QueryFilter:
    severity: Optional[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    correlation_id: Optional[str] = None
    custom_field_filters: Optional[Dict[str, Union[str, int, float, bool]]] = None

    def to_dict(self) -> Dict:
        """Convert QueryFilter to a dictionary for serialization."""
        data = {}
        if self.severity:
            data["severity"] = self.severity
        if self.start_time:
            data["start_time"] = self.start_time.isoformat()
        if self.end_time:
            data["end_time"] = self.end_time.isoformat()
        if self.correlation_id:
            data["correlation_id"] = self.correlation_id
        if self.custom_field_filters:
            data.update(self.custom_field_filters)
        return data


@dataclass
class LogQueryResult:
    entries: List[LogEntry]
    next_page_token: Optional[str] = None

    @classmethod
    def from_dict(cls, data: Dict) -> "LogQueryResult":
        """Create LogQueryResult from a dictionary."""
        entries = []
        for entry in data.get("entries", []):
            timestamp = datetime.fromisoformat(entry["timestamp"])
            severity = entry["severity"]
            message = entry["message"]
            service = entry["service"]
            correlation_id = entry.get("correlation_id")
            custom_fields = {
                k: v for k, v in entry.items() 
                if k not in {"timestamp", "severity", "message", "service", "correlation_id"}
            }
            entries.append(
                LogEntry(
                    timestamp=timestamp,
                    severity=severity,
                    message=message,
                    service=service,
                    correlation_id=correlation_id,
                    custom_fields=custom_fields if custom_fields else None,
                )
            )
        return cls(entries=entries, next_page_token=data.get("next_page_token"))