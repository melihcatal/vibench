from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, Optional


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def normalize_timestamp(value: Optional[str] = None) -> str:
    return value or utc_now_iso()


def normalize_severity(severity: Optional[str]) -> str:
    return (severity or "INFO").upper()


def build_log_payload(
    message: str,
    severity: str = "INFO",
    service: str = "app",
    correlation_id: Optional[str] = None,
    extra: Optional[Mapping[str, Any]] = None,
) -> Dict[str, Any]:
    payload = {
        "timestamp": utc_now_iso(),
        "service": service,
        "severity": normalize_severity(severity),
        "message": message,
    }
    if correlation_id:
        payload["correlation_id"] = correlation_id
    if extra:
        payload.update(dict(extra))
    return payload


def parse_log_events(items: Iterable[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    return [dict(item) for item in items]


@dataclass
class LogQueryResult:
    items: List[Dict[str, Any]]
    next_token: Optional[str] = None
