import datetime
import json


def create_structured_log_entry(
    message: str,
    severity: str,
    component: str,
    data: dict = None,
    correlation_id: str = None,
):
    """
    Creates a structured log entry for Google Cloud Logging.
    """
    log_entry = {
        "message": message,
        "severity": severity.upper(),
        "component": component,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
    }
    if data:
        log_entry.update(data)
    if correlation_id:
        log_entry["correlation_id"] = correlation_id
    return log_entry


def parse_log_entry(entry):
    """
    Parses a log entry from Google Cloud Logging.
    """
    payload = entry.get("jsonPayload", {})
    if not payload:
        payload = {
            "message": entry.get("textPayload", entry.get("insertId"))
        }  # Fallback for non-json logs

    return {
        "timestamp": entry.get("timestamp"),
        "severity": entry.get("severity"),
        "message": payload.get("message"),
        "component": payload.get("component"),
        "correlation_id": payload.get("correlation_id"),
        "data": {
            k: v
            for k, v in payload.items()
            if k not in ["message", "severity", "component", "correlation_id"]
        },
        "resource_type": entry.get("resource", {}).get("type"),
        "resource_labels": entry.get("resource", {}).get("labels", {}),
    }
