from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def iso_utc(value: Optional[datetime] = None) -> str:
    return (value or datetime.now(timezone.utc)).isoformat()


def normalize_event(event: Dict[str, Any]) -> Dict[str, Any]:
    data = dict(event)
    if "timestamp" not in data:
        data["timestamp"] = iso_utc()
    return data


@dataclass
class LogWriteResult:
    index: str
    id: str
    result: str


@dataclass
class LogQueryResult:
    hits: List[Dict[str, Any]]
    total: int


def as_payload(value: Any) -> Dict[str, Any]:
    return asdict(value) if hasattr(value, "__dataclass_fields__") else dict(value)
