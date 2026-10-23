from typing import Dict, Any, List, Optional

class CloudWatchConfig(Dict[str, str]):
    pass

class StructuredLogData(Dict[str, Any]):
    level: str
    message: str
    service: Optional[str] = None
    correlation_id: Optional[str] = None

LogEvent = Dict[str, Any]
QueryResultRaw = List[List[Dict[str, Any]]]
QueryResult = List[Dict[str, Any]]
