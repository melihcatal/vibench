from typing import TypedDict, Dict, Any, List, Optional


class LogData(TypedDict):
    message: str
    status: str
    service: str
    correlation_id: Optional[str]
    env: Optional[str]
    user_id: Optional[int]


class DatadogLogEntry(TypedDict):
    id: str
    attributes: Dict[str, Any]
