"""
observability_models.py

Define local request, response, and normalization helpers for
Managed Log Query / Log Ingestion via Amazon CloudWatch Logs.
"""

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
import json


# ---------------------------------------------------------------------------
# Request models
# ---------------------------------------------------------------------------

@dataclass
class LogEvent:
    """Represents a single structured log event ready for ingestion."""
    message: str
    structured_fields: Dict[str, Any] = field(default_factory=dict)
    timestamp_ms: Optional[int] = None

    def to_cloudwatch_event(self) -> Dict[str, Any]:
        ts = self.timestamp_ms or int(datetime.now(timezone.utc).timestamp() * 1000)
        payload = {
            "timestamp": ts,
            "message": self.message,
        }
        payload.update(self.structured_fields)
        return payload


@dataclass
class CorrelatedLogGroup:
    """A set of log events sharing a correlation / request ID."""
    correlation_id: str
    events: List[LogEvent] = field(default_factory=list)

    def add_event(self, event: LogEvent) -> None:
        event.structured_fields["correlation_id"] = self.correlation_id
        self.events.append(event)


@dataclass
class LogQueryParams:
    """Parameters for a CloudWatch Logs Insights query."""
    log_group_name: str
    query_string: str
    hours_back: int = 1
    limit: int = 100


# ---------------------------------------------------------------------------
# Response models
# ---------------------------------------------------------------------------

@dataclass
class LogQueryResult:
    """A parsed single log record returned from a query."""
    timestamp: Optional[str] = None
    level: Optional[str] = None
    message: Optional[str] = None
    source: Optional[str] = None
    correlation_id: Optional[str] = None
    raw_fields: Dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_cloudwatch_record(
        cls,
        cw_record: List[Dict[str, str]],
    ) -> "LogQueryResult":
        """
        Normalize a CloudWatch Logs Insights row into a LogQueryResult.

        Each cw_record is a list of {"field": str, "value": str} dicts.
        """
        field_map: Dict[str, str] = {}
        for item in cw_record:
            field_map[item["field"]] = item["value"]

        raw_fields = {
            k: v for k, v in field_map.items()
            if k not in ("@timestamp", "@message", "@logStream", "@log")
        }

        return cls(
            timestamp=field_map.get("@timestamp"),
            level=field_map.get("level"),
            message=field_map.get("@message"),
            source=field_map.get("@logStream"),
            correlation_id=field_map.get("correlation_id"),
            raw_fields=raw_fields,
        )


@dataclass
class QueryResponse:
    """Collection of results from a log query."""
    results: List[LogQueryResult] = field(default_factory=list)
    total_matches: int = 0

    def to_dicts(self) -> List[Dict[str, Any]]:
        return [asdict(r) for r in self.results]

    def to_json(self) -> str:
        return json.dumps(self.to_dicts(), indent=2, default=str)


# ---------------------------------------------------------------------------
# Query-string builder helpers
# ---------------------------------------------------------------------------

def build_error_query(
    hours_back: int = 1,
    log_level_filter: Optional[str] = "ERROR",
    extra_filters: Optional[List[str]] = None,
    limit: int = 200,
) -> str:
    """
    Build a CloudWatch Logs Insights query string for error logs.

    Args:
        hours_back: How many trailing hours to search.
        log_level_filter: Severity string to match (e.g. ERROR, FATAL).
        extra_filters: Additional filter expressions.
        limit: Maximum result rows.

    Returns:
        Complete Insights query string.
    """
    lines = [
        "fields @timestamp, @message, level, correlation_id",
        f"filter level = \"{log_level_filter}\"" if log_level_filter else "fields @timestamp, @message",
        f"sort @timestamp desc",
        f"limit {limit}",
    ]
    if extra_filters:
        for f_expr in extra_filters:
            lines.insert(1, f"filter {f_expr}")
    return "\n| ".join(lines)


def build_field_filter_query(
    field_name: str,
    field_value: str,
    hours_back: int = 1,
    limit: int = 100,
) -> str:
    """
    Build a CloudWatch Logs Insights query filtering by a named field.
    """
    return (
        f"fields @timestamp, @message, {field_name}\n"
        f"| filter {field_name} = \"{field_value}\"\n"
        f"| sort @timestamp desc\n"
        f"| limit {limit}"
    )
