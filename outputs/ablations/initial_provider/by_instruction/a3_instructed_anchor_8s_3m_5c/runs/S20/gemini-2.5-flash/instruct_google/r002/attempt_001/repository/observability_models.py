from typing import Dict, Any, List

def normalize_log_entry(entry: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalizes a log entry for consistent processing.
    This is a placeholder for any common transformations or field remapping.

    Args:
        entry (Dict[str, Any]): The raw log entry.

    Returns:
        Dict[str, Any]: The normalized log entry.
    """
    # Example: ensuring a 'timestamp' field exists and is in a standard format
    # In Google Cloud Logging, timestamp is typically 'timestamp' and already RFC3339
    normalized = {
        "timestamp": entry.get("timestamp"),
        "severity": entry.get("severity", "UNKNOWN"),
        "message": entry.get("textPayload") or entry.get("jsonPayload", {}).get("message") or str(entry.get("jsonPayload") or entry.get("protoPayload") or entry.get("structPayload") or ""),
        "resource_type": entry.get("resource", {}).get("type"),
        "resource_labels": entry.get("resource", {}).get("labels", {}),
        "labels": entry.get("labels", {}),
        "log_name": entry.get("logName"),
        "insert_id": entry.get("insertId"),
        **entry # Include all original fields
    }
    return normalized

def create_structured_log_payload(message: str, severity: str = "INFO", **kwargs) -> Dict[str, Any]:
    """
    Creates a structured log payload suitable for ingestion.

    Args:
        message (str): The primary message for the log entry.
        severity (str): The severity of the log entry (e.g., "INFO", "ERROR", "WARNING").
        **kwargs: Additional fields to include in the structured log entry.

    Returns:
        Dict[str, Any]: A dictionary representing the structured log payload.
    """
    payload = {
        "message": message,
        "severity": severity,
        "event_timestamp": datetime.now(timezone.utc).isoformat(timespec='milliseconds') + 'Z',
        **kwargs
    }
    return payload
