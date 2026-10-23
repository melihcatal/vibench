from datetime import datetime
from typing import Any, Dict, Optional
from google.cloud import logging_v2
from observability_client import build_log_name, build_logging_client, load_observability_config
from observability_models import StructuredLogEvent, normalize_timestamp


def write_structured_log(message: str, severity: str = "INFO", payload: Optional[Dict[str, Any]] = None, correlation_id: Optional[str] = None) -> str:
    config = load_observability_config()
    client = build_logging_client(config)
    logger = client.logger(build_log_name(config, "structured"))
    event = StructuredLogEvent(severity=severity, message=message, payload=payload or {}, correlation_id=correlation_id, timestamp=normalize_timestamp(None))
    logger.log_struct(event.to_json_payload(), severity=severity, timestamp=event.timestamp)
    return event.message
