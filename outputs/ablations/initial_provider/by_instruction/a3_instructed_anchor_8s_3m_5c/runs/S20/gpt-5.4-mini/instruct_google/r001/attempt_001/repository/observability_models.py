from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def normalize_timestamp(value: Optional[datetime] = None) -> str:
    dt = value or datetime.now(timezone.utc)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat().replace('+00:00', 'Z')


def build_structured_log_payload(message: str, severity: str = 'INFO', **fields: Any) -> Dict[str, Any]:
    payload = {'message': message, 'severity': severity, 'timestamp': normalize_timestamp()}
    payload.update(fields)
    return payload


@dataclass
class LogQuery:
    project_id: str
    filter_expression: str
    page_size: int = 50


@dataclass
class LogEntryView:
    timestamp: str
    severity: str
    message: str
    labels: Dict[str, Any]


def entries_to_dicts(entries: List[LogEntryView]) -> List[Dict[str, Any]]:
    return [entry.__dict__ for entry in entries]
