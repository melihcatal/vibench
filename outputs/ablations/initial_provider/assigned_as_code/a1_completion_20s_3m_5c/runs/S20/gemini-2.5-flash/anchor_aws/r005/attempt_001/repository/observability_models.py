import dataclasses
import datetime
from typing import Any, Dict, List, Optional


@dataclasses.dataclass
class LogEntry:
    timestamp_ms: int
    message: str
    log_stream_name: str
    event_id: Optional[str] = None
    ingestion_time_ms: Optional[int] = None

@dataclasses.dataclass
class StructuredLogEvent:
    event: Dict[str, Any]
    timestamp_ms: Optional[int] = None

@dataclasses.dataclass
class QueryResults:
    results: List[List[Dict[str, str]]]
    status: str
    next_token: Optional[str] = None

@dataclasses.dataclass
class FilteredLogEvent:
    message: str
    timestamp: datetime.datetime
    log_stream_name: str
    ingestion_time: datetime.datetime
    event_id: str
    log_group_name: str
