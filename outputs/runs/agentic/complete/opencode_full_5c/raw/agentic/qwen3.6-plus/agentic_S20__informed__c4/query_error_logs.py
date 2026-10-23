import os
from datetime import datetime, timezone, timedelta

import requests

DD_SITE = os.getenv("DD_SITE", "datadoghq.com")
DD_API_KEY = os.getenv("DD_API_KEY")
DD_APP_KEY = os.getenv("DD_APP_KEY")
DD_LOGS_QUERY_URL = f"https://api.{DD_SITE}/api/v2/logs/events/search"


def get_dd_query_headers():
    return {
        "DD-API-KEY": DD_API_KEY,
        "DD-APPLICATION-KEY": DD_APP_KEY,
        "Content-Type": "application/json",
    }


def build_query_body(
    query_filter,
    time_from=None,
    time_to=None,
    limit=50,
    sort="timestamp",
):
    now = datetime.now(timezone.utc)
    if time_from is None:
        time_from = now - timedelta(hours=1)
    if time_to is None:
        time_to = now

    body = {
        "filter": {
            "query": query_filter,
            "from": time_from.isoformat(),
            "to": time_to.isoformat(),
        },
        "page": {
            "limit": limit,
        },
        "sort": sort,
    }
    return body


def query_datadog_error_logs(
    severity="error",
    service=None,
    time_from=None,
    time_to=None,
    limit=50,
    additional_filters=None,
):
    query_parts = [f"status:{severity}"]
    if service:
        query_parts.append(f"service:{service}")
    if additional_filters:
        query_parts.extend(additional_filters)

    query_filter = " AND ".join(query_parts)

    body = build_query_body(
        query_filter=query_filter,
        time_from=time_from,
        time_to=time_to,
        limit=limit,
    )

    response = requests.post(
        DD_LOGS_QUERY_URL,
        headers=get_dd_query_headers(),
        json=body,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def query_error_logs(
    severity="error",
    service=None,
    time_from=None,
    time_to=None,
    limit=50,
    additional_filters=None,
):
    return query_datadog_error_logs(
        severity=severity,
        service=service,
        time_from=time_from,
        time_to=time_to,
        limit=limit,
        additional_filters=additional_filters,
    )
