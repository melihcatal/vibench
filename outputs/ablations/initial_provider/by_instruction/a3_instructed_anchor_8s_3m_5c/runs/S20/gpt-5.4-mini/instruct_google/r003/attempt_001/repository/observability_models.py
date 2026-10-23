from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def normalize_severity(severity: Optional[str]) -> str:
    value = (severity or "INFO").strip().upper()
    allowed = {"DEBUG", "INFO", "NOTICE", "WARNING", "ERROR", "CRITICAL", "ALERT", "EMERGENCY"}
    return value if value in allowed else "INFO"


def normalize_labels(labels: Optional[Dict[str, Any]]) -> Dict[str, str]:
    if not labels:
        return {}
    return {str(k): str(v) for k, v in labels.items() if v is not None}


def normalize_log_entry(payload: Dict[str, Any], severity: Optional[str] = None) -> Dict[str, Any]:
    entry = dict(payload)
    entry["severity"] = normalize_severity(severity or entry.get("severity"))
    entry.setdefault("timestamp", utc_now_iso())
    return entry


@dataclass
class LogWriteRequest:
    log_name: str
    payload: Dict[str, Any]
    severity: str = "INFO"


@dataclass
class LogQueryRequest:
    log_name: str
    start_time: str
    end_time: str
    severity: Optional[str] = None
    filters: Optional[Dict[str, Any]] = None


@dataclass
class LogQueryResponse:
    entries: List[Dict[str, Any]]
    next_page_token: str = ""


def extract_message(entry: Dict[str, Any]) -> str:
    for key in ("message", "textPayload", "jsonPayload"):
        if key in entry and entry[key] is not None:
            return str(entry[key])
    return ""


def as_field_filters(filters: Optional[Dict[str, Any]]) -> List[str]:
    if not filters:
        return []
    parts = []
    for key, value in filters.items():
        if value is None:
            continue
        if isinstance(value, str):
            parts.append(f'{key}="{value}"')
        else:
            parts.append(f"{key}={value}")
    return parts
