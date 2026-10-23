import os
from datetime import datetime, timezone


def get_datadog_api_key():
    return os.environ.get("DD_API_KEY", "")


def get_datadog_app_key():
    return os.environ.get("DD_APP_KEY", "")


def get_datadog_site():
    return os.environ.get("DD_SITE", "datadoghq.com")


def get_datadog_logs_api_url():
    site = get_datadog_site()
    return f"https://api.{site}/api/v2/logs/events"


def get_datadog_query_api_url():
    site = get_datadog_site()
    return f"https://api.{site}/api/v2/logs/events/search"


def build_datadog_headers():
    return {
        "Content-Type": "application/json",
        "DD-API-KEY": get_datadog_api_key(),
        "DD-APPLICATION-KEY": get_datadog_app_key(),
    }


def build_log_payload(service, message, level, attributes=None):
    payload = {
        "ddtags": f"service:{service},env:{os.environ.get('DD_ENV', 'production')}",
        "hostname": os.environ.get("DD_HOSTNAME", "localhost"),
        "service": service,
        "message": message,
        "ddsource": "python",
        "status": level.lower(),
        "timestamp": int(datetime.now(timezone.utc).timestamp() * 1000),
    }
    if attributes:
        payload["attributes"] = attributes
    return payload


def build_query_payload(
    filters=None, time_from=None, time_to=None, limit=50, sort="timestamp"
):
    query_filter = {}
    if filters:
        query_filter["query"] = " ".join(filters)
    if time_from:
        query_filter["from"] = time_from
    if time_to:
        query_filter["to"] = time_to
    return {
        "filter": query_filter,
        "sort": sort,
        "page": {"limit": limit},
    }


def normalize_log_entry(raw_entry):
    attributes = raw_entry.get("attributes", {})
    return {
        "id": raw_entry.get("id", ""),
        "timestamp": attributes.get("timestamp", ""),
        "status": attributes.get("status", attributes.get("level", "")),
        "service": attributes.get("service", ""),
        "message": attributes.get("message", ""),
        "host": attributes.get("host", ""),
        "attributes": attributes,
    }
