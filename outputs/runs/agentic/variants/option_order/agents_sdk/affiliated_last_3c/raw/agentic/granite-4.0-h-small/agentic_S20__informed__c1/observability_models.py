from typing import TypedDict, List, Any

class LogEntry(TypedDict):
    """Normalized LogEntry representation used by downstream components."""
    timestamp: str  # ISO 8601 string
    severity: str
    message: str
    correlation_id: str | None
    # Any additional fields can be added here as needed

class LogBatch(List[LogEntry]):
    """Collection of normalized log entries for batch processing."""

def normalize_entry(entry: Any) -> LogEntry:
    """Convert a raw provider‑specific log entry into the normalized LogEntry."""
    # Example transformation for Google Cloud Logging entry dict
    ts = entry.get("timestamp", entry.get("time", ""))
    return {
        "timestamp": ts,
        "severity": entry.get("severity", "UNKNOWN").upper(),
        "message": entry.get("jsonPayload", {}).get("message", ""),
        "correlation_id": entry.get("jsonPayload", {}).get("correlation_id"),
        # Add other fields as needed
    } as LogEntry

if __name__ == "__main__":
    # Simple demo: create a dummy entry and normalize it
    dummy = {
        "timestamp": "2024-08-15T12:34:56Z",
        "severity": "INFO",
        "jsonPayload": {
            "message": "Demo log message",
            "correlation_id": "req-demo-001"
        }
    }
    print(normalize_entry(dummy))
