import os
from typing import Optional


DATADOG_API_HOST = os.getenv("DATADOG_API_HOST", "api.datadoghq.com")
DATADOG_API_KEY = os.getenv("DATADOG_API_KEY", "")
DATADOG_APP_KEY = os.getenv("DATADOG_APP_KEY", "")
DATADOG_SITE = os.getenv("DATADOG_SITE", "datadoghq.com")
DATADOG_SERVICE = os.getenv("DATADOG_SERVICE", "default-service")
DATADOG_SOURCE = os.getenv("DATADOG_SOURCE", "python-observability-client")
DATADOG_LOG_INTAKE_ENDPOINT = f"https://http-intake.logs.{DATADOG_SITE}/api/v2/logs"
DATADOG_LOG_QUERY_ENDPOINT = f"https://{DATADOG_API_HOST}/api/v2/logs/events/search"


def get_datadog_headers():
    return {
        "DD-API-KEY": DATADOG_API_KEY,
        "DD-APPLICATION-KEY": DATADOG_APP_KEY,
        "Content-Type": "application/json",
    }


def get_datadog_log_intake_headers():
    return {
        "DD-API-KEY": DATADOG_API_KEY,
        "Content-Type": "application/json",
    }


def build_datadog_log_payload(
    message: str,
    level: str = "info",
    service: Optional[str] = None,
    hostname: Optional[str] = None,
    ddsource: Optional[str] = None,
    ddtags: Optional[str] = None,
    custom_attributes: Optional[dict] = None,
):
    payload = {
        "message": message,
        "ddsource": ddsource or DATADOG_SOURCE,
        "service": service or DATADOG_SERVICE,
        "status": level.lower(),
    }
    if hostname:
        payload["hostname"] = hostname
    if ddtags:
        payload["ddtags"] = ddtags
    if custom_attributes:
        for key, value in custom_attributes.items():
            payload[key] = value
    return payload


def build_datadog_query_payload(
    query: str,
    time_from: str,
    time_to: str,
    limit: int = 50,
    sort: str = "timestamp",
):
    payload = {
        "filter": {
            "query": query,
            "from": time_from,
            "to": time_to,
        },
        "options": {
            "limit": limit,
            "sort": sort,
        },
    }
    return payload
