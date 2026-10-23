from typing import Dict, Any, Optional, List
from datetime import datetime
import json


class LogEntry:
    def __init__(
        self,
        message: str,
        severity: str,
        timestamp: Optional[datetime] = None,
        correlation_id: Optional[str] = None,
        custom_fields: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.severity = severity
        self.timestamp = timestamp or datetime.utcnow()
        self.correlation_id = correlation_id
        self.custom_fields = custom_fields or {}

    def to_dict(self) -> Dict[str, Any]:
        entry = {
            "message": self.message,
            "severity": self.severity,
            "timestamp": self.timestamp.isoformat() + "Z",
            **self.custom_fields,
        }
        if self.correlation_id:
            entry["correlation_id"] = self.correlation_id
        return entry


class LogQuery:
    def __init__(
        self,
        filter_severity: Optional[str] = None,
        time_from: Optional[datetime] = None,
        time_to: Optional[datetime] = None,
        custom_filters: Optional[Dict[str, Any]] = None,
    ):
        self.filter_severity = filter_severity
        self.time_from = time_from
        self.time_to = time_to
        self.custom_filters = custom_filters or {}

    def to_query_dict(self) -> Dict[str, Any]:
        query = {}
        if self.filter_severity:
            query["severity"] = self.filter_severity
        if self.time_from:
            query["time_from"] = self.time_from.isoformat() + "Z"
        if self.time_to:
            query["time_to"] = self.time_to.isoformat() + "Z"
        query.update(self.custom_filters)
        return query


class LogResponse:
    def __init__(self, entries: List[Dict[str, Any]]):
        self.entries = entries

    @classmethod
    def from_google_logging(cls, entries: List[Any]) -> "LogResponse":
        normalized = []
        for entry in entries:
            normalized.append({
                "message": entry.payload.get("message", ""),
                "severity": entry.severity.name,
                "timestamp": entry.timestamp.isoformat() + "Z",
                "correlation_id": entry.payload.get("correlation_id"),
                **entry.payload,
            })
        return cls(normalized)

    @classmethod
    def from_aws_logs(cls, events: List[Dict[str, Any]]) -> "LogResponse":
        normalized = []
        for event in events:
            payload = json.loads(event.get("message", "{}"))
            normalized.append({
                "message": payload.get("message", ""),
                "severity": payload.get("severity", "INFO"),
                "timestamp": datetime.utcfromtimestamp(event["timestamp"] / 1000).isoformat() + "Z",
                "correlation_id": payload.get("correlation_id"),
                **payload,
            })
        return cls(normalized)