
import json
from datetime import datetime
from typing import Any, Dict, List, Optional

# --- Request Models ---

class LogEntry:
    """Represents a single log entry for ingestion into a logging service."""
    def __init__(self, message: str, severity: str = "INFO", timestamp: Optional[datetime] = None, resource: Optional[Dict[str, str]] = None, labels: Optional[Dict[str, str]] = None, json_payload: Optional[Dict[str, Any]] = None):
        self.message = message
        self.severity = severity
        self.timestamp = timestamp if timestamp else datetime.utcnow()
        self.resource = resource if resource is not None else {"type": "global", "labels": {}}
        self.labels = labels if labels is not None else {}
        self.json_payload = json_payload

    def to_google_cloud_logging_format(self) -> Dict[str, Any]:
        """Converts the log entry to Google Cloud Logging's WriteLogEntries format."""
        entry = {
            "textPayload": self.message,
            "severity": self.severity,
            "timestamp": self.timestamp.isoformat() + "Z", # rfc3339 format
            "resource": self.resource,
            "labels": self.labels,
        }
        if self.json_payload:
            entry["jsonPayload"] = self.json_payload
        return entry

# --- Response Models ---

class LogIngestionResponse:
    """Represents the response from a log ingestion API call."""
    def __init__(self, success: bool, entry_count: int = 0, errors: Optional[List[Dict[str, Any]]] = None):
        self.success = success
        self.entry_count = entry_count
        self.errors = errors if errors is not None else []

    @classmethod
    def from_google_cloud_logging_response(cls, response_data: Dict[str, Any]) -> "LogIngestionResponse":
        """Parses a Google Cloud Logging WriteLogEntries response."""
        # Google Cloud Logging's write method typically returns an empty JSON object on success.
        # Errors are usually raised as exceptions by the client library or indicated in HTTP status codes.
        # For a more robust local helper, we can simulate success or parse a hypothetical error structure.
        if not response_data: # Assuming an empty dict means success
            return cls(success=True, entry_count=1) # Assuming 1 entry if successful
        else:
            # This part would be highly dependent on the actual error structure returned by the API
            # For now, a simplified error representation.
            return cls(success=False, errors=[{"code": 500, "message": "Unknown error from service"}])

# --- Normalization Helpers ---

def normalize_log_entry_for_query(log_entry: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalizes a log entry dictionary for consistent querying.
    This is a placeholder and would be expanded based on specific query requirements
    and the structure of the ingested logs (e.g., flatten nested JSON, standardize field names).
    """
    normalized_entry = log_entry.copy()
    # Example: Ensure timestamp is always present and in a query-friendly format
    if "timestamp" in normalized_entry and isinstance(normalized_entry["timestamp"], str):
        try:
            # Convert to datetime object if it's a string, for easier comparison
            normalized_entry["timestamp"] = datetime.fromisoformat(normalized_entry["timestamp"].replace('Z', '+00:00'))
        except ValueError:
            pass # Keep as string if parsing fails
    
    # Example: If 'jsonPayload' exists, promote its fields for easier querying
    if "jsonPayload" in normalized_entry and isinstance(normalized_entry["jsonPayload"], dict):
        for key, value in normalized_entry["jsonPayload"].items():
            # Avoid overwriting top-level fields unless intended
            if key not in normalized_entry:
                normalized_entry[key] = value
        del normalized_entry["jsonPayload"] # Remove original nested payload

    return normalized_entry

