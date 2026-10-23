from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, Optional


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def normalize_severity(severity: Optional[str]) -> str:
    return (severity or "INFO").strip().upper()


def build_log_event(
    message: str, severity: str = "INFO", **fields: Any
) -> Dict[str, Any]:
    event = {
        "message": message,
        "severity": normalize_severity(severity),
        "timestamp": utc_now_iso(),
    }
    event.update(fields)
    return event


def normalize_query_filters(
    filters: Optional[Mapping[str, Any]] = None,
) -> Dict[str, Any]:
    return {k: v for k, v in (filters or {}).items() if v not in (None, "")}


@dataclass
class LogWriteResult:
    success: bool
    request_id: Optional[str] = None
    raw: Optional[Any] = None


@dataclass
class LogQueryResult:
    items: List[Dict[str, Any]]
    raw: Optional[Any] = None


def extract_items(payload: Any) -> List[Dict[str, Any]]:
    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]
    if isinstance(payload, dict):
        for key in ("items", "logs", "entries", "results", "data"):
            value = payload.get(key)
            if isinstance(value, list):
                return [item for item in value if isinstance(item, dict)]
        return [payload]
    return []
