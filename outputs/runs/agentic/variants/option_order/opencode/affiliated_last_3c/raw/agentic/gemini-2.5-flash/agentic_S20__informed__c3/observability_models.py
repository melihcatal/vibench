from typing import Dict, Any, Optional


class LogEntry:
    def __init__(
        self,
        message: str,
        severity: str = "INFO",
        labels: Optional[Dict[str, str]] = None,
        json_payload: Optional[Dict[str, Any]] = None,
        trace_id: Optional[str] = None,
    ):
        self.message = message
        self.severity = severity
        self.labels = labels if labels is not None else {}
        self.json_payload = json_payload
        self.trace_id = trace_id


class LogQuery:
    def __init__(
        self, filter_string: str, order_by: str = "timestamp desc", limit: int = 100
    ):
        self.filter_string = filter_string
        self.order_by = order_by
        self.limit = limit
