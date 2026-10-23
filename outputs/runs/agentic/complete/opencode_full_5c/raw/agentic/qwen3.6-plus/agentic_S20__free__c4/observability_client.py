import json
import os
import socket
from datetime import datetime, timezone
from datadog_api_client import Configuration
from datadog_api_client.v2.model.http_log import HTTPLog
from observability_models import StructuredLogEvent, CorrelatedLogEvent


DATADOG_API_HOST = os.environ.get("DD_SITE", "api.datadoghq.com")


def get_datadog_config(
    api_key: str | None = None, app_key: str | None = None
) -> Configuration:
    api_key = api_key or os.environ.get("DD_API_KEY", "")
    app_key = app_key or os.environ.get("DD_APP_KEY", "")
    config = Configuration()
    config.api_key["apiKeyAuth"] = api_key
    config.api_key["appKeyAuth"] = app_key
    config.server_variables = {"site": DATADOG_API_HOST}
    return config


def build_log_payload(event: StructuredLogEvent) -> dict:
    tags = [
        f"level:{event.level}",
        f"service:{event.service}",
        f"source:{event.source}",
        f"event_id:{event.event_id}",
    ]
    payload = {
        "message": event.message,
        "ddtags": ",".join(tags),
        "hostname": socket.gethostname(),
        "service": event.service,
        "source": event.source,
        "status": event.level,
        "timestamp": event.timestamp.isoformat(),
        "event_id": event.event_id,
    }
    payload.update(event.custom_attributes)
    return payload


def build_correlated_log_payload(
    event: CorrelatedLogEvent,
    correlation_id: str,
    service: str,
) -> dict:
    tags = [
        f"level:{event.level}",
        f"service:{service}",
        f"source:{event.source}",
        f"correlation_id:{correlation_id}",
        f"event_id:{event.event_id}",
    ]
    payload = {
        "message": event.message,
        "ddtags": ",".join(tags),
        "hostname": socket.gethostname(),
        "service": service,
        "source": event.source,
        "status": event.level,
        "timestamp": event.timestamp.isoformat(),
        "event_id": event.event_id,
        "correlation_id": correlation_id,
    }
    payload.update(event.custom_attributes)
    return payload


def normalize_datadog_log_entry(log_item) -> dict:
    attributes = log_item.attributes
    raw_message = attributes.get("message", "")
    if isinstance(raw_message, dict):
        message = json.dumps(raw_message)
    else:
        message = str(raw_message)

    timestamp_attr = attributes.get("timestamp", "")
    if isinstance(timestamp_attr, int):
        timestamp = datetime.fromtimestamp(
            timestamp_attr / 1000, tz=timezone.utc
        ).isoformat()
    elif isinstance(timestamp_attr, str):
        timestamp = timestamp_attr
    else:
        timestamp = datetime.now(timezone.utc).isoformat()

    tags = attributes.get("tags", [])
    level = "info"
    for tag in tags:
        if tag.startswith("level:"):
            level = tag.split(":", 1)[1]
            break

    status = attributes.get("status", level)
    if status and status.lower() != level:
        level = status.lower()

    custom_attrs = {}
    for key, value in attributes.items():
        if key not in (
            "message",
            "timestamp",
            "status",
            "tags",
            "service",
            "source",
            "host",
        ):
            custom_attrs[key] = value

    return {
        "event_id": attributes.get("event_id", ""),
        "timestamp": timestamp,
        "message": message,
        "level": level,
        "service": attributes.get("service", ""),
        "source": attributes.get("source", ""),
        "attributes": custom_attrs,
    }
