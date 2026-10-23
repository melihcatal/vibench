from typing import Dict, Any, Optional, List
from datetime import datetime
import json


class LogEntry:
    def __init__(
        self,
        message: str,
        severity: str,
        timestamp: datetime,
        correlation_id: Optional[str] = None,
        custom_fields: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.severity = severity
        self.timestamp = timestamp
        self.correlation_id = correlation_id
        self.custom_fields = custom_fields or {}

    def to_dict(self) -> Dict[str, Any]:
        payload = {
            "message": self.message,
            "severity": self.severity,
            "timestamp": self.timestamp.isoformat(),
            **self.custom_fields,
        }
        if self.correlation_id:
            payload["correlation_id"] = self.correlation_id
        return payload


class LogQuery:
    def __init__(
        self,
        severity_filter: Optional[List[str]] = None,
        time_range_start: Optional[datetime] = None,
        time_range_end: Optional[datetime] = None,
        field_filters: Optional[Dict[str, Any]] = None,
    ):
        self.severity_filter = severity_filter or []
        self.time_range_start = time_range_start
        self.time_range_end = time_range_end
        self.field_filters = field_filters or {}

    def to_query_dict(self) -> Dict[str, Any]:
        query = {}
        if self.severity_filter:
            query["severity"] = {"in": self.severity_filter}
        if self.time_range_start and self.time_range_end:
            query["timestamp"] = {
                "gte": self.time_range_start.isoformat(),
                "lte": self.time_range_end.isoformat(),
            }
        for field, value in self.field_filters.items():
            query[field] = {"eq": value}
        return query


class LogResponse:
    def __init__(self, entries: List[Dict[str, Any]]):
        self.entries = entries

    @classmethod
    def from_google_logging(cls, entries: List[Any]) -> "LogResponse":
        normalized = []
        for entry in entries:
            payload = {
                "message": entry.payload.get("message", ""),
                "severity": entry.severity.name,
                "timestamp": entry.timestamp.isoformat(),
                **entry.payload,
            }
            normalized.append(payload)
        return cls(normalized)

    @classmethod
    def from_azure_monitor(cls, entries: List[Dict[str, Any]]) -> "LogResponse":
        normalized = []
        for entry in entries:
            payload = {
                "message": entry.get("message", ""),
                "severity": entry.get("severityLevel", "INFO"),
                "timestamp": entry.get("timeGenerated", ""),
                **entry,
            }
            normalized.append(payload)
        return cls(normalized)

    def to_list(self) -> List[Dict[str, Any]]:
        return self.entries