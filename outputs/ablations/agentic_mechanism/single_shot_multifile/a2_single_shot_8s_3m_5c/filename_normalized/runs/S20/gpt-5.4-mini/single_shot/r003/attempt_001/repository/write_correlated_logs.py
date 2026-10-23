from datetime import datetime
from typing import Iterable, Mapping, Optional
from google.cloud import logging_v2
from observability_client import build_log_name, build_logging_client, load_observability_config
from observability_models import StructuredLogEvent, normalize_timestamp


def write_correlated_logs(request_id: str, events: Iterable[Mapping[str, object]], severity: str = "INFO") -> int:
    config = load_observability_config()
    client = build_logging_client(config)
    logger = client.logger(build_log_name(config, "correlated"))
    count = 0
    for item in events:
        message = str(item.get("message", ""))
        payload = {k: v for k, v in item.items() if k != "message"}
        payload["request_id"] = request_id
        event = StructuredLogEvent(severity=severity, message=message, payload=payload, correlation_id=request_id, timestamp=normalize_timestamp(None))
        logger.log_struct(event.to_json_payload(), severity=severity, timestamp=event.timestamp)
        count += 1
    return count
