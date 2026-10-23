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


def build_fetch_query_body(
    query_filter,
    time_from=None,
    time_to=None,
    limit=100,
    sort="-timestamp",
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


def fetch_datadog_recent_logs(
    field_filters=None,
    time_from=None,
    time_to=None,
    limit=100,
    sort="-timestamp",
):
    query_parts = []
    if field_filters:
        for key, value in field_filters.items():
            query_parts.append(f"{key}:{value}")

    query_filter = " AND ".join(query_parts) if query_parts else "*"

    body = build_fetch_query_body(
        query_filter=query_filter,
        time_from=time_from,
        time_to=time_to,
        limit=limit,
        sort=sort,
    )

    response = requests.post(
        DD_LOGS_QUERY_URL,
        headers=get_dd_query_headers(),
        json=body,
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


def fetch_recent_logs(
    field_filters=None,
    time_from=None,
    time_to=None,
    limit=100,
    sort="-timestamp",
):
    return fetch_datadog_recent_logs(
        field_filters=field_filters,
        time_from=time_from,
        time_to=time_to,
        limit=limit,
        sort=sort,
    )
