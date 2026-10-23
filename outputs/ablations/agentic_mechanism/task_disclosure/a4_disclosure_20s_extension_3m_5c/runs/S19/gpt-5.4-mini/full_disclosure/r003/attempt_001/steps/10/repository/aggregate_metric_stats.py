import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Dict, Optional

import requests


@dataclass
class MetricStats:
    count: int
    min: float
    max: float
    avg: float
    sum: float
    start: datetime
    end: datetime


def _isoformat(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def aggregate_metric_stats(
    metric_name: str,
    *,
    minutes: int = 60,
    resource: Optional[str] = None,
    dimensions: Optional[Dict[str, str]] = None,
) -> MetricStats:
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
        params={"from": int(start.timestamp()), "to": int(end.timestamp()), "query": query},
        headers={"DD-API-KEY": api_key, "DD-APPLICATION-KEY": app_key},
        timeout=30,
    )
    response.raise_for_status()
    payload = response.json()

    values = []
    for item in payload.get("series", []):
        for _, value in item.get("pointlist", []):
            if value is not None:
                values.append(float(value))

    if not values:
        raise RuntimeError("No datapoints returned for the requested metric window")

    total = sum(values)
    return MetricStats(
        count=len(values),
        min=min(values),
        max=max(values),
        avg=total / len(values),
        sum=total,
        start=start,
        end=end,
    )


if __name__ == "__main__":
    raise SystemExit("Import aggregate_metric_stats and call aggregate_metric_stats().")
