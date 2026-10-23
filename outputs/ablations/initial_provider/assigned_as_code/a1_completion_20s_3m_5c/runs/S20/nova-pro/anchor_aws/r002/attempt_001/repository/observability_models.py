from typing import Any, Dict


def normalize_log_event(event: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "timestamp_ms": event.get("timestamp", 0),
        "message": event.get("message", ""),
    }


def parse_log_response(response: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "submitted": response.get("acceptedLogEvents", 0) > 0,
        "rejected": response.get("rejectedLogEventsInfo", {}),
    }