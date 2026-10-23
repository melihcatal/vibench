from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, Optional

@dataclass
class LogEntry:
    log_name: str
    resource_type: str
    resource_labels: Dict[str, str]
    timestamp: datetime
    severity: str
    json_payload: Optional[Dict[str, Any]] = field(default_factory=dict)
    text_payload: Optional[str] = None
    insert_id: Optional[str] = None
    trace: Optional[str] = None
    span_id: Optional[str] = None
    receive_timestamp: Optional[datetime] = None

@dataclass
class QueryFilter:
    project_id: str
    log_name: Optional[str] = None
    severity: Optional[str] = None
    time_range_start: Optional[datetime] = None
    time_range_end: Optional[datetime] = None
    free_text_search: Optional[str] = None
    correlation_id: Optional[str] = None

    def to_filter_string(self) -> str:
        filters = [f"project="{self.project_id}""]
        if self.log_name:
            filters.append(f"logName="projects/{self.project_id}/logs/{self.log_name}"")
        if self.severity:
            filters.append(f"severity>="{self.severity}"")
        if self.time_range_start:
            filters.append(f"timestamp>="{self.time_range_start.isoformat()}Z"")
        if self.time_range_end:
            filters.append(f"timestamp<="{self.time_range_end.isoformat()}Z"")
        if self.free_text_search:
            filters.append(f"text:("{self.free_text_search}"")")
        if self.correlation_id:
            filters.append(f"jsonPayload.correlationId="{self.correlation_id}"")
        return " AND ".join(filters)

