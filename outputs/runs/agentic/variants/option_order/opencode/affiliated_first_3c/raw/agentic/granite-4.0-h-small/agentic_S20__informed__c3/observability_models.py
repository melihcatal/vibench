from dataclasses import dataclass
from datetime import datetime
from typing import Any, List


@dataclass
class LogEntry:
    timestamp: datetime  # use UTC by default
    level: str
    message: str
    correlation_id: str | None = None
    extra: dict[str, Any] = None
    # Add any additional fields required by your provider's schema


@dataclass
class QueryFilter:
    expression: str


class QueryResult:
    entries: List[dict]
    total: int
    page_token: str | None = None


@dataclass
class LogSearchResult(QueryResult):
    # Inherits from QueryResult
    pass
