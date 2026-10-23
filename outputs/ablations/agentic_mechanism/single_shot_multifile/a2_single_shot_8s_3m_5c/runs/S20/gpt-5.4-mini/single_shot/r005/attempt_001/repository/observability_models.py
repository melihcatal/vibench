from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Optional


def _isoformat(value: datetime) -> str:
    if value.tzinfo is None:
        value = value.replace(tzinfo=timezone.utc)
    return value.astimezone(timezone.utc).isoformat()


def normalize_dict_payload(payload: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    if not payload:
        return {}
    return {str(k): v for k, v in payload.items() if v is not None}


@dataclass
class StructuredLogEvent:
    message: str
    severity: str
    service: str
    source: str
    correlation_id: str
    fields: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def to_payload(self, namespace: str) -> Dict[str, Any]:
        return {
            "namespace": namespace,
            "timestamp": _isoformat(self.timestamp),
            "message": self.message,
            "severity": self.severity,
            "service": self.service,
            "source": self.source,
            "correlation_id": self.correlation_id,
            "fields": normalize_dict_payload(self.fields),
        }


@dataclass
class LogQueryRequest:
    query: str
    start_time: datetime
    end_time: datetime
    limit: int
    namespace: str
    filters: Dict[str, Any] = field(default_factory=dict)

    def to_payload(self) -> Dict[str, Any]:
        return {
            "namespace": self.namespace,
            "query": self.query,
            "start_time": _isoformat(self.start_time),
            "end_time": _isoformat(self.end_time),
            "limit": self.limit,
            "filters": normalize_dict_payload(self.filters),
        }