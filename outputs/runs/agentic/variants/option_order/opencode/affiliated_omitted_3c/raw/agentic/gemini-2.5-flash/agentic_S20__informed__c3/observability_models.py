from typing import Dict, Any, List, Optional
from datetime import datetime


class LogEvent:
    """Represents a single log event with a message and optional fields."""

    def __init__(
        self,
        message: str,
        timestamp: Optional[datetime] = None,
        fields: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.timestamp = timestamp if timestamp else datetime.utcnow()
        self.fields = fields if fields else {}

    def to_aws_cloudwatch_event(self) -> Dict[str, Any]:
        """Converts the log event to the format expected by AWS CloudWatch Logs."""
        return {
            "timestamp": int(
                self.timestamp.timestamp() * 1000
            ),  # CloudWatch expects milliseconds
            "message": self.message,
        }


class StructuredLog(LogEvent):
    """A log event with a specific structure for easier parsing."""

    def __init__(
        self,
        message: str,
        level: str,
        service: str,
        timestamp: Optional[datetime] = None,
        fields: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message, timestamp, fields)
        self.level = level
        self.service = service
        self.fields["level"] = level
        self.fields["service"] = service

    def to_aws_cloudwatch_event(self) -> Dict[str, Any]:
        """Converts the structured log event to the format expected by AWS CloudWatch Logs."""
        # Embed structured fields into the message for simpler ingestion
        # In a real scenario, you might send JSON string as message and parse later
        structured_message = {
            "message": self.message,
            "level": self.level,
            "service": self.service,
            **self.fields,
        }
        return {
            "timestamp": int(self.timestamp.timestamp() * 1000),
            "message": str(structured_message),  # CloudWatch expects string message
        }


class CorrelatedLog(LogEvent):
    """A log event that includes a correlation ID."""

    def __init__(
        self,
        message: str,
        correlation_id: str,
        timestamp: Optional[datetime] = None,
        fields: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(message, timestamp, fields)
        self.correlation_id = correlation_id
        self.fields["correlation_id"] = correlation_id

    def to_aws_cloudwatch_event(self) -> Dict[str, Any]:
        """Converts the correlated log event to the format expected by AWS CloudWatch Logs."""
        correlated_message = {
            "message": self.message,
            "correlation_id": self.correlation_id,
            **self.fields,
        }
        return {
            "timestamp": int(self.timestamp.timestamp() * 1000),
            "message": str(correlated_message),
        }


class LogQuery:
    """Defines parameters for querying logs."""

    def __init__(
        self,
        log_group_names: List[str],
        start_time: datetime,
        end_time: datetime,
        query_string: str,
    ):
        self.log_group_names = log_group_names
        self.start_time = start_time
        self.end_time = end_time
        self.query_string = query_string


class LogQueryResult:
    """Represents the result of a log query."""

    def __init__(self, records: List[Dict[str, Any]], status: str, query_id: str):
        self.records = records
        self.status = status
        self.query_id = query_id
