
import datetime
from typing import Any, Dict, List, Optional, Union

class LogEntry:
    """Represents a single log entry for ingestion."""
    def __init__(self, timestamp: datetime.datetime, message: str, level: str = "INFO", metadata: Optional[Dict[str, Any]] = None):
        self.timestamp = timestamp
        self.message = message
        self.level = level
        self.metadata = metadata if metadata is not None else {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "message": self.message,
            "level": self.level,
            "metadata": self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "LogEntry":
        return cls(
            timestamp=datetime.datetime.fromisoformat(data["timestamp"]),
            message=data["message"],
            level=data.get("level", "INFO"),
            metadata=data.get("metadata", {})
        )

class LogQueryResult:
    """Represents a single log entry returned from a query."""
    def __init__(self, timestamp: datetime.datetime, message: str, level: str, resource_id: str, metadata: Dict[str, Any]):
        self.timestamp = timestamp
        self.message = message
        self.level = level
        self.resource_id = resource_id
        self.metadata = metadata

    def to_dict(self) -> Dict[str, Any]:
        return {
            "timestamp": self.timestamp.isoformat(),
            "message": self.message,
            "level": self.level,
            "resource_id": self.resource_id,
            "metadata": self.metadata
        }

def normalize_log_entry(entry: Dict[str, Any]) -> LogEntry:
    """Normalizes a raw dictionary into a LogEntry object."""
    return LogEntry.from_dict(entry)

def normalize_query_result(result: Dict[str, Any]) -> LogQueryResult:
    """Normalizes a raw dictionary into a LogQueryResult object."""
    return LogQueryResult(
        timestamp=datetime.datetime.fromisoformat(result["timestamp"]),
        message=result["message"],
        level=result.get("level", "INFO"),
        resource_id=result["resource_id"],
        metadata=result.get("metadata", {})
    )

class LogIngestionRequest:
    """Represents a request to ingest logs."""
    def __init__(self, entries: List[LogEntry], source: str):
        self.entries = entries
        self.source = source

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entries": [entry.to_dict() for entry in self.entries],
            "source": self.source
        }

class LogIngestionResponse:
    """Represents a response from a log ingestion operation."""
    def __init__(self, success: bool, ingested_count: int, errors: Optional[List[str]] = None):
        self.success = success
        self.ingested_count = ingested_count
        self.errors = errors if errors is not None else []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "ingested_count": self.ingested_count,
            "errors": self.errors
        }

def normalize_ingestion_response(response: Dict[str, Any]) -> LogIngestionResponse:
    """Normalizes a raw dictionary into a LogIngestionResponse object."""
    return LogIngestionResponse(
        success=response.get("success", False),
        ingested_count=response.get("ingested_count", 0),
        errors=response.get("errors", [])
    )

class LogQueryRequest:
    """Represents a request to query logs."""
    def __init__(self, query_string: str, start_time: Optional[datetime.datetime] = None,
                 end_time: Optional[datetime.datetime] = None, limit: int = 100,
                 resource_ids: Optional[List[str]] = None):
        self.query_string = query_string
        self.start_time = start_time
        self.end_time = end_time
        self.limit = limit
        self.resource_ids = resource_ids if resource_ids is not None else []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "query_string": self.query_string,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "limit": self.limit,
            "resource_ids": self.resource_ids
        }

class LogQueryResponse:
    """Represents a response from a log query operation."""
    def __init__(self, results: List[LogQueryResult], total_results: int, next_page_token: Optional[str] = None):
        self.results = results
        self.total_results = total_results
        self.next_page_token = next_page_token

    def to_dict(self) -> Dict[str, Any]:
        return {
            "results": [result.to_dict() for result in self.results],
            "total_results": self.total_results,
            "next_page_token": self.next_page_token
        }

def normalize_query_response(response: Dict[str, Any]) -> LogQueryResponse:
    """Normalizes a raw dictionary into a LogQueryResponse object."""
    return LogQueryResponse(
        results=[normalize_query_result(r) for r in response.get("results", [])],
        total_results=response.get("total_results", 0),
        next_page_token=response.get("next_page_token")
    )
