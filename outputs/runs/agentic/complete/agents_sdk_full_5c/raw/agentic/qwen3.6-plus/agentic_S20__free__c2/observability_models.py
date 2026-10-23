"""Define local request, response, and normalization helpers for Managed Log Query / Log Ingestion."""

import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from typing import Optional, Any


@dataclass
class LogEvent:
    """Normalized log event for managed log ingestion."""
    message: str
    service: str = "default-service"
    status: str = "info"
    hostname: Optional[str] = None
    source: Optional[str] = None
    correlation_id: Optional[str] = None
    tags: Optional[list] = field(default_factory=list)
    custom_attributes: dict = field(default_factory=dict)
    timestamp: Optional[datetime] = None

    def to_dict(self) -> dict:
        """Serialize to a dictionary suitable for provider ingestion."""
        data = asdict(self)
        if self.timestamp is not None:
            data["timestamp"] = int(self.timestamp.timestamp())
        else:
            data["timestamp"] = int(datetime.now(timezone.utc).timestamp())
        if self.tags:
            data["tags"] = ",".join(self.tags)
        if self.source:
            data["ddsource"] = self.source
        data.pop("custom_attributes", None)
        merged = {k: v for k, v in data.items() if v is not None}
        merged.update(self.custom_attributes)
        return merged


@dataclass
class LogQueryRequest:
    """Normalized query parameters for log retrieval."""
    query: str = ""
    from_ts: Optional[int] = None
    to_ts: Optional[int] = None
    limit: int = 100
    sort: str = "timestamp"
    filter: Optional[dict] = None

    def to_provider_params(self) -> dict:
        """Convert to provider-specific query parameters."""
        params = {
            "filter[query]": self.query,
            "filter[from]": self.from_ts,
            "filter[to]": self.to_ts,
            "page[limit]": self.limit,
            "sort": self.sort,
        }
        return {k: v for k, v in params.items() if v is not None}


@dataclass
class LogQueryResponse:
    """Normalized response wrapper for log query results."""
    logs: list = field(default_factory=list)
    total_count: int = 0
    next_page_token: Optional[str] = None

    @classmethod
    def from_provider(cls, provider_response: dict, provider: str = "datadog") -> "LogQueryResponse":
        """Normalize provider-specific response into a standard format."""
        if provider == "datadog":
            data = provider_response.get("data", [])
            logs = []
            for entry in data:
                attrs = entry.get("attributes", {})
                log_entry = {
                    "message": attrs.get("message", ""),
                    "status": attrs.get("status", "unknown"),
                    "service": attrs.get("service", ""),
                    "timestamp": attrs.get("timestamp", ""),
                    "hostname": attrs.get("host", ""),
                    "attributes": attrs.get("attributes", {}),
                    "tags": attrs.get("tags", []),
                }
                logs.append(log_entry)
            total = provider_response.get("meta", {}).get("page", {}).get("total_matched", len(logs))
            next_token = provider_response.get("meta", {}).get("page", {}).get("after")
            return cls(logs=logs, total_count=total, next_page_token=next_token)
        return cls(logs=provider_response.get("logs", []), total_count=provider_response.get("total", 0))


def generate_correlation_id() -> str:
    """Generate a unique correlation/trace identifier for log correlation."""
    return str(uuid.uuid4())


def build_error_query(service: Optional[str] = None, time_range_minutes: int = 30) -> str:
    """Build a Datadog Logs query string for error logs."""
    query = "status:error"
    if service:
        query += f" service:{service}"
    return query


def build_recent_query(filters: Optional[dict] = None) -> str:
    """Build a query string with field filters for recent log retrieval."""
    parts = []
    if filters:
        for key, value in filters.items():
            parts.append(f"{key}:{value}")
    return " ".join(parts) if parts else "*"
