from __future__ import annotations
import datetime
from typing import Any, Dict


class LogEntry:
    """Normalized log entry model from IBM Cloud Logs."""
    def __init__(self, raw: Dict[str, Any]) -> None:
        self.raw = raw
        self.timestamp = datetime.datetime.fromisoformat(raw['timestamp'].replace('Z', '+00:00'))
        self.severity = raw.get('severity', 'INFO')
        self.message = raw.get('message', '')
        self.correlation_id = raw.get('correlation_id')
        # Add any custom fields you need here

    def __repr__(self) -> str:
        return f"LogEntry(timestamp={self.timestamp}, severity={self.severity}, message={self.message})"


class QueryResult:
    """Wrapper for a query response from the logging service."""
    def __init__(self, raw: Dict[str, Any]) -> None:
        self.raw = raw
        self.hits = [LogEntry(hit) for hit in raw.get('logs', [])]
        self.total = raw.get('total', 0)


class SearchResult:
    """Wrapper for a search response."""
    def __init__(self, raw: Dict[str, Any]) -> None:
        self.raw = raw
        self.hits = [LogEntry(hit) for hit in raw.get('hits', [])]
        self.total = raw.get('total', 0)
