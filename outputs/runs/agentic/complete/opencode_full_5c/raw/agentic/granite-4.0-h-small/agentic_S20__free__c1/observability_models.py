from __future__ import annotations
import dataclasses
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, List


@dataclasses.dataclass(frozen=True)
class LogEvent:
    """Normalized log event ready for ingestion."""

    event_id: str = dataclasses.field(default_factory=uuid.uuid4)
    message: str = ""
    severity: str = "INFO"
    timestamp: int = dataclasses.field(
        default_factory=lambda: int(datetime.now(timezone.utc).timestamp() * 1000)
    )
    request_id: str | None = None

    def to_dict(self) -> Dict[str, Any]:
        return dataclasses.asdict(self)


@dataclasses.dataclass(frozen=True)
class LogQuery:
    """Parameters for a log query request."""

    start_time: int
    end_time: int
    severity: str | None = None
    field_filters: Dict[str, Any] | None = None

    def to_dict(self) -> Dict[str, Any]:
        return dataclasses.asdict(self)


@dataclasses.dataclass(frozen=True)
class LogResult:
    """Parsed result from a log query."""

    events: List[Dict[str, Any]]
    cursor: str | None = None

    @classmethod
    def from_response(cls, response: Dict[str, Any]) -> LogResult:
        return cls(
            events=response.get("events", []),
            cursor=response.get("cursor"),
        )
