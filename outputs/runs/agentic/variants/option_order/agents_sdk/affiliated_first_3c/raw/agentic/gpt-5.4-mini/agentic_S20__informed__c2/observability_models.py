from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class LogEvent:
    message: str
    service: str
    severity: str = "info"
    timestamp: Optional[datetime] = None
    correlation_id: Optional[str] = None
    request_id: Optional[str] = None
    fields: Dict[str, Any] = field(default_factory=dict)

    def to_datadog(self) -> Dict[str, Any]:
        ts = self.timestamp or datetime.now(timezone.utc)
        payload: Dict[str, Any] = {
            "message": self.message,
            "service": self.service,
            "status": self.severity,
            "timestamp": ts.astimezone(timezone.utc).isoformat(),
        }
        if self.correlation_id:
            payload["correlation_id"] = self.correlation_id
        if self.request_id:
            payload["request_id"] = self.request_id
        payload.update(self.fields)
        return payload


@dataclass
class LogEntry:
    message: str
    service: str
    severity: str
    timestamp: str
    fields: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_datadog(cls, item: Dict[str, Any]) -> "LogEntry":
        attributes = item.get("attributes", item)
        message = attributes.get("message", "")
        service = attributes.get("service", attributes.get("service_name", "unknown"))
        severity = attributes.get("status", attributes.get("severity", "info"))
        timestamp = attributes.get("timestamp", attributes.get("date", ""))
        reserved = {"message", "service", "service_name", "status", "severity", "timestamp", "date"}
        fields = {k: v for k, v in attributes.items() if k not in reserved}
        return cls(message=message, service=service, severity=severity, timestamp=timestamp, fields=fields)


@dataclass
class QueryResult:
    entries: List[LogEntry]

    @classmethod
    def from_datadog(cls, payload: Dict[str, Any]) -> "QueryResult":
        data = payload.get("data", []) or []
        entries = [LogEntry.from_datadog(item) for item in data]
        return cls(entries=entries)


def normalize_log_event(event: LogEvent) -> Dict[str, Any]:
    return event.to_datadog()


def summarize_messages(entries: Iterable[LogEntry]) -> str:
    messages = [entry.message for entry in entries if entry.message]
    return "; ".join(messages[:5])
