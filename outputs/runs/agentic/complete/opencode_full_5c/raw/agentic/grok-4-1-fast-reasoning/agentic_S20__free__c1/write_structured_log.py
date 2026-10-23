import json
import time
from observability_client import put_structured_log
from typing import Dict, Any


def write_structured_log(
    level: str = "INFO",
    event_type: str = "app_event",
    data: Dict[str, Any] = None,
    correlation_id: str = None,
):
    if data is None:
        data = {}
    return put_structured_log(level, event_type, data, correlation_id)


if __name__ == "__main__":
    success = write_structured_log(
        level="INFO",
        event_type="user_action",
        data={"action": "login", "user_id": "u123"},
        correlation_id="sess-456",
    )
    print(f"Structured log written successfully: {success}")
