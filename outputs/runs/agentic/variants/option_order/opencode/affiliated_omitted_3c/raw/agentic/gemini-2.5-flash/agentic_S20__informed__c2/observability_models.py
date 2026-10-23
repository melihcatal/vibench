import dataclasses
import datetime
from typing import Any, Dict, List, Optional


@dataclasses.dataclass
class LogEvent:
    message: str
    timestamp: Optional[int] = None  # Unix timestamp in milliseconds
    attributes: Optional[Dict[str, Any]] = None


@dataclasses.dataclass
class LogQuery:
    log_group_name: str
    start_time: datetime.datetime
    end_time: datetime.datetime
    filter_pattern: Optional[str] = None


@dataclasses.dataclass
class LogQueryResult:
    timestamp: datetime.datetime
    message: str
    fields: Dict[str, Any]
