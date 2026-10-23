from typing import Dict, Any, List


def create_log_entry(
    message: str, severity: str = "DEFAULT", custom_fields: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Creates a structured log entry payload.
    """
    entry = {
        "text_payload": message,
        "severity": severity,
    }
    if custom_fields:
        entry["json_payload"] = custom_fields
    return entry


def create_correlated_log_entry(
    message: str,
    correlation_id: str,
    severity: str = "DEFAULT",
    custom_fields: Dict[str, Any] = None,
) -> Dict[str, Any]:
    """
    Creates a structured log entry with a correlation ID.
    """
    if custom_fields is None:
        custom_fields = {}

    custom_fields["correlation_id"] = correlation_id

    # For Google Cloud Logging, trace is a specific field for correlation.
    # The format is projects/PROJECT_ID/traces/TRACE_ID
    project_id = custom_fields.get("project_id", "default-project")
    trace_id = f"projects/{project_id}/traces/{correlation_id}"

    entry = {
        "text_payload": message,
        "severity": severity,
        "json_payload": custom_fields,
        "trace": trace_id,
    }
    return entry


def format_log_entries(entries: List[Any]) -> List[Dict[str, Any]]:
    """
    Formats log entries from the API into a more readable format.
    """
    formatted_entries = []
    for entry in entries:
        formatted = {
            "timestamp": entry.timestamp.isoformat(),
            "severity": entry.severity.name
            if hasattr(entry.severity, "name")
            else entry.severity,
            "payload": entry.json_payload or entry.text_payload,
            "trace": entry.trace,
        }
        formatted_entries.append(formatted)
    return formatted_entries
