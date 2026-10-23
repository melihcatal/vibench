from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def normalize_fields(fields: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    return dict(fields or {})


@dataclass
class LogEvent:
    message: str
    severity: str = "INFO"
    service: str = "orders-api"
    correlation_id: Optional[str] = None
    timestamp: str = ""
    fields: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        data = asdict(self)
        data["timestamp"] = data["timestamp"] or utc_now_iso()
        data["fields"] = normalize_fields(data["fields"])
        return data


@dataclass
class LogQuery:
    query: str
    start_time: str
    end_time: str
    severity: Optional[str] = None
    limit: int = 100


@dataclass
class LogResponse:
    items: List[Dict[str, Any]]
    provider: str
