import json
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _drop_none(value: Dict[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in value.items() if v is not None}


@dataclass
class StructuredLogEvent:
    message: str
    severity: str = "info"
    service: Optional[str] = None
    correlation_id: Optional[str] = None
    fields: Optional[Dict[str, Any]] = None
    timestamp: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return _drop_none({"message": self.message, "severity": self.severity, "service": self.service, "correlation_id": self.correlation_id, "fields": self.fields or {}, "timestamp": self.timestamp or utc_now_iso()})


@dataclass
class LogQuery:
    severity: Optional[str] = None
    field_filters: Optional[Dict[str, Any]] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    limit: int = 25

    def to_dict(self) -> Dict[str, Any]:
        return _drop_none({"severity": self.severity, "field_filters": self.field_filters or {}, "start_time": self.start_time, "end_time": self.end_time, "limit": self.limit})


def normalize_log_result(item: Dict[str, Any]) -> Dict[str, Any]:
    normalized = dict(item)
    if "timestamp" not in normalized and "@timestamp" in normalized:
        normalized["timestamp"] = normalized.pop("@timestamp")
    if isinstance(normalized.get("fields"), str):
        try:
            normalized["fields"] = json.loads(normalized["fields"])
        except json.JSONDecodeError:
            pass
    return normalized


def normalize_results(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [normalize_log_result(item) for item in items]
