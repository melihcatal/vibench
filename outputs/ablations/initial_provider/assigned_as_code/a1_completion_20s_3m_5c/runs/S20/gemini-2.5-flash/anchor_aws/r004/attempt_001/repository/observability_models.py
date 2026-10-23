import json
from typing import Dict, Any

def normalize_log_event(event: Dict[str, Any]) -> Dict[str, Any]:
    """Normalizes a log event dictionary for ingestion."""
    # In a real application, this would involve more robust schema validation and transformation
    return {
        "timestamp": event.get("timestamp_ms"),
        "message": json.dumps(event.get("event")),
    }

def parse_log_entry(log_event: Dict[str, Any]) -> Dict[str, Any]:
    """Parses a log entry retrieved from the logging service."""
    message = log_event.get("message", "{}")
    try:
        parsed_message = json.loads(message)
    except json.JSONDecodeError:
        parsed_message = {"raw_message": message}
    
    return {
        "timestamp": log_event.get("timestamp"),
        "event": parsed_message,
        "logStreamName": log_event.get("logStreamName"),
        "logGroupName": log_event.get("logGroupName"),
    }
