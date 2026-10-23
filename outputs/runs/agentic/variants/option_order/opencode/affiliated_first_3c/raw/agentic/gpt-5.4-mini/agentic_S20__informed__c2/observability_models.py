from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, Optional


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_severity(severity: str) -> str:
    return severity.strip().upper()


def build_log_record(message: str, severity: str, **fields: Any) -> Dict[str, Any]:
    record = {
        "message": message,
        "severity": normalize_severity(severity),
        "timestamp": utc_now_iso(),
    }
    record.update(fields)
    return record


def coerce_time_range(
    start_time: Optional[str], end_time: Optional[str]
) -> Dict[str, Optional[str]]:
    return {"start_time": start_time, "end_time": end_time}


@dataclass
class LogQuery:
    query: str
    start_time: Optional[str] = None
    end_time: Optional[str] = None


@dataclass
class LogResult:
    items: List[Dict[str, Any]]
    raw: Any = None
