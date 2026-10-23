import os
from datetime import datetime, timezone

from google.cloud import logging_v2


def load_config(config=None):
    config = dict(config or {})
    config.setdefault("project_id", os.environ.get("GOOGLE_CLOUD_PROJECT") or os.environ.get("GCP_PROJECT"))
    config.setdefault("log_name", os.environ.get("OBSERVABILITY_LOG_NAME", "application-log"))
    config.setdefault("region", os.environ.get("GOOGLE_CLOUD_REGION"))
    if not config.get("project_id"):
        raise ValueError("project_id is required")
    return config


def build_client(config=None):
    config = load_config(config)
    return logging_v2.Client(project=config["project_id"]), config


def to_datetime(value):
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.astimezone(timezone.utc)
    if isinstance(value, (int, float)):
        if value > 10**12:
            value = value / 1000.0
        return datetime.fromtimestamp(value, tz=timezone.utc)
    if isinstance(value, str):
        return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)
    raise TypeError("unsupported datetime value")


def isoformat(value):
    dt = to_datetime(value)
    return dt.isoformat().replace("+00:00", "Z") if dt else None
