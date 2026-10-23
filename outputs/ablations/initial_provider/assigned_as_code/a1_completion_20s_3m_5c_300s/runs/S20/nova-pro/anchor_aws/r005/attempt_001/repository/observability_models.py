from typing import Any, Dict


def normalize_log_event(event: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "timestamp_ms": event.get("timestamp", None),
        "message": event.get("message", None),
        "correlation_id": event.get("correlation_id", None),
    }
