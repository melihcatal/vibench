from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_timestamp(value: Optional[str]) -> str:
    return value or utc_now_iso()


def normalize_severity(value: Optional[str]) -> str:
    return (value or "INFO").upper()


def normalize_text(value: Optional[str]) -> str:
    return (value or "").strip()


@dataclass
class LogEvent:
    timestamp: str
    severity: str
    message: str
    service: str
    correlation_id: Optional[str] = None
    attributes: Optional[Dict[str, Any]] = None

    def to_payload(self) -> Dict[str, Any]:
        payload = {
            "timestamp": normalize_timestamp(self.timestamp),
            "severity": normalize_severity(self.severity),
            "message": normalize_text(self.message),
            "service": normalize_text(self.service),
        }
        if self.correlation_id:
            payload["correlation_id"] = normalize_text(self.correlation_id)
        if self.attributes:
            payload["attributes"] = self.attributes
        return payload


def build_query_filter(field: str, value: str) -> Dict[str, Any]:
    return {"field": field, "value": value}


def ensure_list(value: Any) -> List[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]
