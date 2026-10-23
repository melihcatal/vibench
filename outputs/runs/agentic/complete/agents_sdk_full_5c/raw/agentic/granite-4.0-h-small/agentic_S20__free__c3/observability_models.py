from typing import TypedDict, List, Any, Dict

# Shared normalized log record model for log ingestion services

class NormalizedLogRecord(TypedDict):
    timestamp: str  # ISO 8601 string
    level: str      # e.g., 'ERROR', 'WARN', 'INFO'
    service: str    # application or service identifier
    message: str    # human‑readable message text
    correlation_id: str = None  # optional request‑trace identifier
    metadata: Dict[str, Any] = None  # free‑form extra fields

# Request model for creating multiple log entries at once
class BulkLogPayload(TypedDict):
    records: List[NormalizedLogRecord]

# Filter model used when querying logs

class LogFilter(TypedDict):
    start_time: str  # ISO 8601 start bound (inclusive)
    end_time: str    # ISO 8601 end bound (exclusive)
    level: str = None
    service: str = None
    correlation_id: str = None
    keyword: str = None  # free‑text string to search in message field

# Simple response envelope for query APIs
class QueryResponse(TypedDict):
    total_hits: int
    logs: List[NormalizedLogRecord]
