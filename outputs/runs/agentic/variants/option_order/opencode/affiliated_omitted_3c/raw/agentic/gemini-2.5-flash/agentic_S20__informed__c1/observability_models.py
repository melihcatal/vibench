from typing import Dict, Any, List, Optional
from datetime import datetime


class LogEvent:
    def __init__(
        self,
        message: str,
        timestamp: Optional[int] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.timestamp = (
            timestamp
            if timestamp is not None
            else int(datetime.now().timestamp() * 1000)
        )
        self.metadata = metadata if metadata is not None else {}

    def to_cloudwatch_event(self) -> Dict[str, Any]:
        return {"timestamp": self.timestamp, "message": self.message}


class StructuredLogEvent(LogEvent):
    def __init__(self, level: str, service: str, message: str, **kwargs):
        super().__init__(message, **kwargs)
        self.level = level
        self.service = service
        self.metadata.update({"level": self.level, "service": self.service})
        self.message = self._format_message()

    def _format_message(self) -> str:
        # CloudWatch Logs can store JSON directly as a string message
        import json

        log_data = {
            "level": self.level,
            "service": self.service,
            "message": self.message,
            "metadata": self.metadata,
        }
        return json.dumps(log_data)


class CorrelatedLogEvent(LogEvent):
    def __init__(self, correlation_id: str, message: str, **kwargs):
        super().__init__(message, **kwargs)
        self.correlation_id = correlation_id
        self.metadata["correlation_id"] = self.correlation_id
        self.message = self._format_message()

    def _format_message(self) -> str:
        import json

        log_data = {
            "correlation_id": self.correlation_id,
            "message": self.message,
            "metadata": self.metadata,
        }
        return json.dumps(log_data)


class LogQueryResponse:
    def __init__(self, events: List[Dict[str, Any]]):
        self.events = events

    def to_list(self) -> List[Dict[str, Any]]:
        return self.events
