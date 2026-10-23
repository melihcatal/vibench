from dataclasses import dataclass
from typing import Dict, Any, Optional, List
from datetime import datetime
import json


@dataclass
class LogEntry:
    timestamp: datetime
    level: str
    message: str
    correlation_id: Optional[str] = None
    extra: Optional[Dict[str, Any]] = None


def parse_query_result(result: List[Dict[str, str]]) -> LogEntry:
    fields = {item["field"]: item["value"] for item in result}
    timestamp_str = fields.get("@timestamp", "")
    if timestamp_str.endswith("Z"):
        timestamp_str = timestamp_str[:-1] + "+00:00"
    timestamp = datetime.fromisoformat(timestamp_str)
    message_str = fields.get("@message", "{}")
    log_dict = json.loads(message_str)
    return LogEntry(
        timestamp=timestamp,
        level=log_dict.get("level", "INFO"),
        message=log_dict.get("message", message_str),
        correlation_id=log_dict.get("correlation_id"),
        extra=log_dict.get("extra"),
    )
