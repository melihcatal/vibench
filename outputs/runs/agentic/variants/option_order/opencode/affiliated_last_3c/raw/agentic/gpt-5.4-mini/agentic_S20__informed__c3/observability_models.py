from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def normalize_text(value: str) -> str:
    return " ".join(value.strip().split())


@dataclass
class LogEvent:
    message: str
    service: str
    source: str
    status: str
    correlation_id: Optional[str] = None
    request_id: Optional[str] = None
    tags: Optional[List[str]] = None
    extra: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        payload: Dict[str, Any] = {
            "message": normalize_text(self.message),
            "service": self.service,
            "source": self.source,
            "status": self.status,
            "timestamp": iso_now(),
        }
        if self.correlation_id:
            payload["correlation_id"] = self.correlation_id
        if self.request_id:
            payload["request_id"] = self.request_id
        if self.tags:
            payload["ddtags"] = ",".join(self.tags)
        if self.extra:
            payload.update(self.extra)
        return payload


def parse_log_hits(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    return payload.get("data", []) or payload.get("results", []) or []


def build_search_params(
    query: str, start: str, end: str, limit: int = 20
) -> Dict[str, Any]:
    return {
        "filter[from]": start,
        "filter[to]": end,
        "filter[query]": query,
        "page[limit]": limit,
    }
