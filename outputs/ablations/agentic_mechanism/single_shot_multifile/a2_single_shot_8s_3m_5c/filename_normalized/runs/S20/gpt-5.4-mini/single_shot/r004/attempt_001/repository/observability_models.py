from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Optional


@dataclass
class LogQueryRequest:
    log_name: str
    severity: Optional[str]
    start_time: datetime
    end_time: datetime
    field_filters: Dict[str, Any]


def _utc_iso(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat()


def normalize_log_event(payload: Dict[str, Any]) -> Dict[str, Any]:
    normalized = dict(payload)
    timestamp = normalized.get("timestamp")
    if isinstance(timestamp, datetime):
        normalized["timestamp"] = _utc_iso(timestamp)
    return normalized


def build_structured_payload(message: str, severity: str, fields: Dict[str, Any], request_id: str, timestamp: datetime) -> Dict[str, Any]:
    payload = {"message": message, "severity": severity, "request_id": request_id, "timestamp": timestamp}
    payload.update(fields)
    return payload


def build_correlated_payload(message: str, severity: str, correlation_id: str, step: str, timestamp: datetime) -> Dict[str, Any]:
    return {
        "message": message,
        "severity": severity,
        "correlation_id": correlation_id,
        "step": step,
        "timestamp": timestamp,
    }


def build_query_request(log_name: str, severity: Optional[str], start_time: datetime, end_time: datetime, field_filters: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "log_name": log_name,
        "severity": severity,
        "start_time": start_time,
        "end_time": end_time,
        "field_filters": field_filters,
    }
