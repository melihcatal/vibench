from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, Any, List, Optional
from enum import Enum


class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


@dataclass
class LogEvent:
    message: str
    level: LogLevel
    timestamp: Optional[datetime] = None
    correlation_id: Optional[str] = None
    service: Optional[str] = None
    environment: Optional[str] = None
    extra_fields: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        result = {
            "message": self.message,
            "level": self.level.value,
            "timestamp": self.timestamp.isoformat()
            if self.timestamp
            else datetime.utcnow().isoformat(),
        }

        if self.correlation_id:
            result["correlation_id"] = self.correlation_id
        if self.service:
            result["service"] = self.service
        if self.environment:
            result["environment"] = self.environment
        if self.extra_fields:
            result.update(self.extra_fields)

        return result

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LogEvent":
        level = LogLevel(data.get("level", "INFO"))
        timestamp_str = data.get("timestamp")
        timestamp = datetime.fromisoformat(timestamp_str) if timestamp_str else None

        return cls(
            message=data.get("message", ""),
            level=level,
            timestamp=timestamp,
            correlation_id=data.get("correlation_id"),
            service=data.get("service"),
            environment=data.get("environment"),
            extra_fields={
                k: v
                for k, v in data.items()
                if k
                not in [
                    "message",
                    "level",
                    "timestamp",
                    "correlation_id",
                    "service",
                    "environment",
                ]
            },
        )


@dataclass
class LogQuery:
    query_string: str
    start_time: datetime
    end_time: datetime
    limit: int = 100

    def to_cloudwatch_insights_query(self) -> Dict[str, Any]:
        return {
            "queryString": self.query_string,
            "startTime": int(self.start_time.timestamp()),
            "endTime": int(self.end_time.timestamp()),
            "limit": self.limit,
        }

    @classmethod
    def create_error_query(cls, hours: int = 1, limit: int = 100) -> "LogQuery":
        end_time = datetime.utcnow()
        start_time = end_time.replace(hour=end_time.hour - hours)
        query_string = "fields @timestamp, @message, level, correlation_id, service | filter level in ['ERROR', 'CRITICAL'] | sort @timestamp desc"
        return cls(query_string, start_time, end_time, limit)

    @classmethod
    def create_recent_logs_query(
        cls, field_filters: Dict[str, str], hours: int = 1, limit: int = 100
    ) -> "LogQuery":
        end_time = datetime.utcnow()
        start_time = end_time.replace(hour=end_time.hour - hours)

        filter_parts = []
        for field, value in field_filters.items():
            filter_parts.append(f"{field} = '{value}'")

        filter_str = " and ".join(filter_parts) if filter_parts else "1=1"
        query_string = f"fields @timestamp, @message, level, correlation_id, service | filter {filter_str} | sort @timestamp desc"

        return cls(query_string, start_time, end_time, limit)


@dataclass
class LogQueryResult:
    query_id: str
    status: str
    results: List[LogEvent]
    statistics: Optional[Dict[str, Any]] = None

    def is_complete(self) -> bool:
        return self.status in ["Complete", "Failed", "Cancelled"]

    def get_error_logs(self) -> List[LogEvent]:
        return [
            log
            for log in self.results
            if log.level in [LogLevel.ERROR, LogLevel.CRITICAL]
        ]

    def get_by_correlation_id(self, correlation_id: str) -> List[LogEvent]:
        return [log for log in self.results if log.correlation_id == correlation_id]


@dataclass
class IncidentSummary:
    incident_id: str
    start_time: datetime
    end_time: datetime
    error_count: int
    unique_services: List[str]
    most_common_errors: List[Dict[str, Any]]
    correlation_ids: List[str]

    def to_report_dict(self) -> Dict[str, Any]:
        return {
            "incident_id": self.incident_id,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat(),
            "error_count": self.error_count,
            "affected_services": self.unique_services,
            "top_errors": self.most_common_errors[:5],
            "related_correlation_ids": self.correlation_ids[:10],
        }
