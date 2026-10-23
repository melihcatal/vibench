import json
import time
from datetime import datetime
from typing import Dict, Any
from observability_client import CloudWatchLogsClient, format_log_message
from observability_models import LogEntry


def write_structured_log(
    level: str,
    message: str,
    log_stream_name: str = "application",
    service: str = "default-service",
    component: str = "default-component",
    **additional_fields,
) -> Dict[str, Any]:
    client = CloudWatchLogsClient()

    log_entry = LogEntry(
        timestamp=datetime.utcnow().isoformat() + "Z",
        level=level,
        message=message,
        service=service,
        component=component,
        metadata=additional_fields,
    )

    log_message = log_entry.to_json()

    response = client.put_log_event(
        log_stream_name=log_stream_name,
        message=log_message,
        timestamp=int(time.time() * 1000),
    )

    return {
        "success": True,
        "message_id": response.get("nextSequenceToken", "unknown"),
        "log_stream": log_stream_name,
        "log_group": client.log_group_name,
        "timestamp": log_entry.timestamp,
    }


def write_info_log(message: str, **kwargs) -> Dict[str, Any]:
    return write_structured_log("INFO", message, **kwargs)


def write_error_log(message: str, **kwargs) -> Dict[str, Any]:
    return write_structured_log("ERROR", message, **kwargs)


def write_warning_log(message: str, **kwargs) -> Dict[str, Any]:
    return write_structured_log("WARNING", message, **kwargs)


def write_debug_log(message: str, **kwargs) -> Dict[str, Any]:
    return write_structured_log("DEBUG", message, **kwargs)


if __name__ == "__main__":
    result = write_structured_log(
        level="INFO",
        message="Application started successfully",
        service="api-gateway",
        component="startup",
        environment="production",
        version="1.2.3",
    )
    print(f"Log written: {result}")
