from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Mapping, Optional


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_level(level: Optional[str]) -> Optional[str]:
    if level is None:
        return None
    return str(level).strip().upper()


def compact_mapping(values: Mapping[str, Any]) -> Dict[str, Any]:
    return {k: v for k, v in values.items() if v is not None}


@dataclass
class StructuredLogEvent:
    timestamp: str
    level: str
    message: str
    fields: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        payload = {"timestamp": self.timestamp, "level": self.level, "message": self.message}
        payload.update(self.fields)
        return payload


@dataclass
class LogQuery:
    group_name: str
    start_time: str
    end_time: str
    filter_pattern: str


@dataclass
class QueryResult:
    events: List[Dict[str, Any]]
    next_token: Optional[str] = None


def coerce_log_items(items: Iterable[Mapping[str, Any]]) -> List[Dict[str, Any]]:
    return [dict(item) for item in items]
