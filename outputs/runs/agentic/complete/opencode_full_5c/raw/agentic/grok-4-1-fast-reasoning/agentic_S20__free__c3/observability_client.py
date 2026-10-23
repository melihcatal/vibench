import time
from typing import Dict, Any, List


def current_timestamp_ms() -> int:
    return int(time.time() * 1000)


def normalize_log_event(event: Dict[str, Any]) -> Dict[str, Any]:
    event = event.copy()
    if "timestamp" not in event:
        event["timestamp"] = current_timestamp_ms()
    if "service" not in event:
        event["service"] = "python-app"
    if "status" not in event:
        event["status"] = "info"
    event["ddsource"] = "python"
    return event


def parse_datadog_logs_response(data: dict) -> List[Dict[str, Any]]:
    logs = []
    if "data" in data and data["data"]:
        query_result = data["data"][0]
        if "logs" in query_result:
            for log_entry in query_result["logs"]:
                attrs = log_entry.get("attributes", {})
                logs.append(attrs)
    return logs


def build_query_string(filters: Dict[str, str], severity: str = None) -> str:
    parts = []
    if severity:
        parts.append(f"status:{severity}")
    for key, value in filters.items():
        parts.append(f"{key}:{value}")
    return " ".join(parts)
