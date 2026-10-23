import os
import json
from datetime import datetime, timezone, timedelta


DD_SITE = os.getenv("DD_SITE", "datadoghq.com")
DD_API_KEY = os.getenv("DD_API_KEY")
DD_APP_KEY = os.getenv("DD_APP_KEY")
DD_SERVICE = os.getenv("DD_SERVICE", "default-service")
DD_ENV = os.getenv("DD_ENV", "production")
DD_LOGS_INTAKE_URL = f"https://http-intake.logs.{DD_SITE}/api/v2/logs"
DD_LOGS_QUERY_URL = f"https://api.{DD_SITE}/api/v2/logs/events/search"


def load_config():
    return {
        "dd_site": DD_SITE,
        "dd_api_key": DD_API_KEY,
        "dd_app_key": DD_APP_KEY,
        "dd_service": DD_SERVICE,
        "dd_env": DD_ENV,
        "logs_intake_url": DD_LOGS_INTAKE_URL,
        "logs_query_url": DD_LOGS_QUERY_URL,
    }


def validate_config():
    missing = []
    if not DD_API_KEY:
        missing.append("DD_API_KEY")
    if not DD_APP_KEY:
        missing.append("DD_APP_KEY")
    if missing:
        raise ValueError(
            f"Missing required Datadog configuration: {', '.join(missing)}"
        )


def get_intake_headers():
    return {
        "DD-API-KEY": DD_API_KEY,
        "Content-Type": "application/json",
    }


def get_query_headers():
    return {
        "DD-API-KEY": DD_API_KEY,
        "DD-APPLICATION-KEY": DD_APP_KEY,
        "Content-Type": "application/json",
    }


def normalize_log_event(raw_event):
    if isinstance(raw_event, dict):
        attributes = raw_event.get("attributes", {})
        tags = attributes.get("tags", [])
        return {
            "timestamp": attributes.get("timestamp"),
            "message": attributes.get("message", ""),
            "status": attributes.get("status", "unknown"),
            "service": attributes.get("service", ""),
            "hostname": attributes.get("hostname", ""),
            "tags": tags if isinstance(tags, list) else [],
            "raw": raw_event,
        }
    return {
        "timestamp": None,
        "message": str(raw_event),
        "status": "unknown",
        "service": "",
        "hostname": "",
        "tags": [],
        "raw": raw_event,
    }


def normalize_query_response(response_data):
    events = response_data.get("data", [])
    return [normalize_log_event(evt) for evt in events]


def build_time_range(hours_back=1):
    now = datetime.now(timezone.utc)
    time_from = now - timedelta(hours=hours_back)
    return time_from, now


def format_query_filter(severity=None, service=None, extra=None):
    parts = []
    if severity:
        parts.append(f"status:{severity}")
    if service:
        parts.append(f"service:{service}")
    if extra:
        parts.extend(extra)
    return " AND ".join(parts) if parts else "*"
