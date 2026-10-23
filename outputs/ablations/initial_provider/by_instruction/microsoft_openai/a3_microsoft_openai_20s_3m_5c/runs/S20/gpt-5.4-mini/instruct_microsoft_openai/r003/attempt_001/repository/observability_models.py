from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, Optional


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')


def normalize_severity(value: Optional[str]) -> str:
    if not value:
        return 'INFO'
    return str(value).upper()


def normalize_event(event: Mapping[str, Any]) -> Dict[str, Any]:
    normalized = dict(event)
    normalized.setdefault('timestamp', utc_now_iso())
    normalized['severity'] = normalize_severity(normalized.get('severity'))
    return normalized


@dataclass
class LogWriteResult:
    status: str
    raw: Dict[str, Any]


@dataclass
class LogQueryResult:
    items: List[Dict[str, Any]]
    raw: Dict[str, Any]
