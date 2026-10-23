import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

import requests


@dataclass
class MetricPoint:
    timestamp: datetime
    value: float


def _isoformat(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def query_metric_window(
    metric_name: str,
    *,
    minutes: int = 60,
    resource: Optional[str] = None,
    dimensions: Optional[Dict[str, str]] = None,
    limit: int = 200,
) -> List[MetricPoint]:
    api_key = os.environ.get("DATADOG_API_KEY")
    app_key = os.environ.get("DATADOG_APP_KEY")
    site = os.environ.get("DATADOG_SITE", "datadoghq.com")
    if not api_key or not app_key:
        raise RuntimeError("DATADOG_API_KEY and DATADOG_APP_KEY are required")

    end = datetime.now(timezone.utc)
    start = end - timedelta(minutes=minutes)

    query_parts = [f"avg:{metric_name}{{*}}"]
    if resource:
        query_parts.append(f"{{resource:{resource}}}")
    if dimensions:
        for key, value in dimensions.items():
            query_parts.append(f"{{{key}:{value}}}")
    query = "".join(query_parts)

    url = f"https://api.{site}/api/v1/query"
    response = requests.get(
        url,
        params={"from": int(start.timestamp()), "to": int(end.timestamp()), "query": query, "page[size]": limit},
        headers={"DD-API-KEY": api_key, "DD-APPLICATION-KEY": app_key},
        timeout=30,
    )
    response.raise_for_status()
    payload: Dict[str, Any] = response.json()

    series = payload.get("series", [])
    points: List[MetricPoint] = []
    for item in series:
        for ts, value in item.get("pointlist", []):
            if value is None:
                continue
            points.append(MetricPoint(timestamp=datetime.fromtimestamp(ts, tz=timezone.utc), value=float(value)))
    points.sort(key=lambda p: p.timestamp)
    return points


if __name__ == "__main__":
    raise SystemExit("Import query_metric_window and call query_metric_window().")
