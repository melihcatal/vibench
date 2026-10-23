import json
from typing import Dict, Any


def parse_cloudwatch_event(cw_event: Dict[str, Any]) -> Dict[str, Any]:
    message_str = cw_event["message"]
    try:
        parsed_data = json.loads(message_str)
    except (json.JSONDecodeError, TypeError):
        parsed_data = {"raw_message": message_str}
    log_event = {
        "timestamp": cw_event["timestamp"] / 1000.0,
        "level": parsed_data.get("level", "INFO"),
        "message": parsed_data.get(
            "message", parsed_data.get("raw_message", message_str)
        ),
    }
    log_event["trace_id"] = parsed_data.get("trace_id")
    if "data" in parsed_data:
        log_event["data"] = parsed_data["data"]
    return log_event
