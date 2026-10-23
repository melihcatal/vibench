import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

import requests


@dataclass
class MetricDatapoint:
    timestamp: str
    value: float
    dimensions: Dict[str, Any]


def _env(name: str, default: Optional[str] = None) -> str:
    value = os.getenv(name, default)
    if value is None:
        raise ValueError(f"Missing required environment variable: {name}")
    return value


def _parse_iso_datetime(value: str) -> datetime:
    dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc)


def query_metric_window(metric_name: str, window_minutes: int = 60, limit: int = 100) -> List[MetricDatapoint]:
    api_key = _env("DATADOG_API_KEY")
    app_key = _env("DATADOG_APP_KEY")
    site = os.getenv("DATADOG_SITE", "datadoghq.com")

    end = datetime.now(timezone.utc)
    start = end - timedelta(minutes=window_minutes)

    url = f"https://api.{site}/api/v1/query"
    params = {
        "from": int(start.timestamp()),
        "to": int(end.timestamp()),
        "query": metric_name,
    }
    headers = {
        "DD-API-KEY": api_key,
        "DD-APPLICATION-KEY": app_key,
        "Accept": "application/json",
    }

    response = requests.get(url, params=params, headers=headers, timeout=30)
    response.raise_for_status()
    payload = response.json()

    series = payload.get("series", [])
    datapoints: List[MetricDatapoint] = []
    for item in series:
        scope = item.get("scope", "")
        dimensions = {"scope": scope} if scope else {}
        for point in item.get("pointlist", [])[:limit]:
            if not point or len(point) < 2 or point[1] is None:
                continue
            timestamp = datetime.fromtimestamp(point[0], tz=timezone.utc).isoformat()
            datapoints.append(
                MetricDatapoint(timestamp=timestamp, value=float(point[1]), dimensions=dimensions)
            )

    datapoints.sort(key=lambda p: _parse_iso_datetime(p.timestamp))
    return datapoints[:limit]


__all__ = ["MetricDatapoint", "query_metric_window"]
