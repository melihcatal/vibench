from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json


@dataclass
class LogEntry:
    timestamp: str
    level: str
    message: str
    correlation_id: Optional[str] = None
    service: Optional[str] = None
    component: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_json(self) -> str:
        return json.dumps(
            {
                "timestamp": self.timestamp,
                "level": self.level,
                "message": self.message,
                "correlation_id": self.correlation_id,
                "service": self.service,
                "component": self.component,
                "metadata": self.metadata,
            }
        )

    @classmethod
    def from_json(cls, json_str: str) -> "LogEntry":
        data = json.loads(json_str)
        return cls(
            timestamp=data.get("timestamp", ""),
            level=data.get("level", "INFO"),
            message=data.get("message", ""),
            correlation_id=data.get("correlation_id"),
            service=data.get("service"),
            component=data.get("component"),
            metadata=data.get("metadata", {}),
        )


@dataclass
class LogQueryRequest:
    start_time: int
    end_time: int
    filter_pattern: Optional[str] = None
    query_string: Optional[str] = None
    limit: int = 100

    def to_cloudwatch_params(self) -> Dict[str, Any]:
        params = {
            "startTime": self.start_time,
            "endTime": self.end_time,
            "limit": self.limit,
        }
        if self.filter_pattern:
            params["filterPattern"] = self.filter_pattern
        if self.query_string:
            params["queryString"] = self.query_string
        return params


@dataclass
class LogQueryResponse:
    query_id: Optional[str] = None
    events: List[Dict[str, Any]] = field(default_factory=list)
    results: List[Dict[str, Any]] = field(default_factory=list)
    status: str = "Unknown"

    def get_normalized_logs(self) -> List[LogEntry]:
        normalized_logs = []
        for event in self.events:
            message = event.get("message", "")
            try:
                log_data = json.loads(message)
                log_entry = LogEntry(
                    timestamp=log_data.get("timestamp", ""),
                    level=log_data.get("level", "INFO"),
                    message=log_data.get("message", message),
                    correlation_id=log_data.get("correlation_id"),
                    service=log_data.get("service"),
                    component=log_data.get("component"),
                    metadata=log_data.get("metadata", {}),
                )
            except json.JSONDecodeError:
                log_entry = LogEntry(
                    timestamp=datetime.fromtimestamp(
                        event.get("timestamp", 0) / 1000
                    ).isoformat(),
                    level="INFO",
                    message=message,
                    metadata={"raw_event": event},
                )
            normalized_logs.append(log_entry)
        return normalized_logs


@dataclass
class ErrorSummary:
    error_count: int = 0
    unique_errors: List[str] = field(default_factory=list)
    services_affected: List[str] = field(default_factory=list)
    time_range: str = ""
    most_common_error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "error_count": self.error_count,
            "unique_errors": self.unique_errors,
            "services_affected": self.services_affected,
            "time_range": self.time_range,
            "most_common_error": self.most_common_error,
        }


def normalize_cloudwatch_event(event: Dict[str, Any]) -> LogEntry:
    message = event.get("message", "")
    timestamp = event.get("timestamp", 0)

    try:
        log_data = json.loads(message)
        return LogEntry(
            timestamp=log_data.get(
                "timestamp", datetime.fromtimestamp(timestamp / 1000).isoformat()
            ),
            level=log_data.get("level", "INFO"),
            message=log_data.get("message", message),
            correlation_id=log_data.get("correlation_id"),
            service=log_data.get("service"),
            component=log_data.get("component"),
            metadata=log_data.get("metadata", {}),
        )
    except json.JSONDecodeError:
        return LogEntry(
            timestamp=datetime.fromtimestamp(timestamp / 1000).isoformat(),
            level="INFO",
            message=message,
            metadata={"raw_event": event},
        )


def create_error_filter_pattern(
    level: str = "ERROR", service: Optional[str] = None
) -> str:
    pattern = f'{{$.level = "{level}"'
    if service:
        pattern += f' && $.service = "{service}"'
    pattern += "}"
    return pattern
