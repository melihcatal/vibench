# HELPER

import os
from datetime import datetime

# This module provides shared configuration and a thin wrapper around Datadog
# Metrics API. It is used by all SAME-SCENARIO files.

# Datadog credentials come from environment variables for production safety
API_KEY = os.getenv("DD_API_KEY")
APP_KEY = os.getenv("DD_APP_KEY")

BASE_URL = "https://api.datadoghq.com/api/v1"


def _request(endpoint, params=None, method="GET"):
    import requests

    url = BASE_URL + endpoint
    if method == "GET":
        resp = requests.get(url, params=params)
    else:
        resp = requests.post(url, json=params)
    resp.raise_for_status()
    return resp.json()


# Simple helper to build a time window


def build_window(
    start: datetime | None = None, end: datetime | None = None, offset_hours: int = 1
):
    if start is None:
        start = datetime.utcnow() - timedelta(hours=offset_hours)
    if end is None:
        end = datetime.utcnow()
    return {
        "from": int(start.timestamp()),
        "to": int(end.timestamp()),
    }
