from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass(frozen=True)
class LogEvent:
    message: str
    service: str
    status: str
    timestamp: str
    correlation_id: Optional[str] = None
    request_id: Optional[str] = None
    attributes: Optional[Dict[str, Any]] = None

    def to_datadog_dict(self) -> Dict[str, Any]:
        payload = {
            "message": self.message,
            "service": self.service,
            "status": self.status,
            "timestamp": self.timestamp,
        }
        if self.correlation_id is not None:
            payload["correlation_id"] = self.correlation_id
        if self.request_id is not None:
            payload["request_id"] = self.request_id
        if self.attributes:
            payload.update(self.attributes)
        return payload


@dataclass(frozen=True)
class LogQueryResult:
    items: List[Dict[str, Any]]
    total: int


@dataclass(frozen=True)
class IncidentSummary:
    severity: str
    time_window: str
    error_count: int
    correlation_ids: List[str]
    messages: List[str]


def normalize_log_items(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    if "data" in payload and isinstance(payload["data"], list):
        return payload["data"]
    if "results" in payload and isinstance(payload["results"], list):
        return payload["results"]
    if "logs" in payload and isinstance(payload["logs"], list):
        return payload["logs"]
    return []
