import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

import requests


@dataclass
class MetricSummary:
    metric: str
    start_time: str
    end_time: str
    sample_count: int
    minimum: Optional[float]
    maximum: Optional[float]
    average: Optional[float]
    latest: Optional[float]
    trend: str
    anomaly_detected: bool
    anomaly_reason: Optional[str]


def _parse_time(value: Optional[str]) -> datetime:
    if value:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed.astimezone(timezone.utc)
    return datetime.now(timezone.utc)


def _infer_trend(values: List[float]) -> str:
    if len(values) < 2:
        return "insufficient-data"
    first = values[0]
    last = values[-1]
    if last > first * 1.05:
        return "increasing"
    if last < first * 0.95:
        return "decreasing"
    return "stable"


def _detect_anomaly(values: List[float]) -> Optional[str]:
    if len(values) < 4:
        return None
    avg = sum(values) / len(values)
    variance = sum((v - avg) ** 2 for v in values) / len(values)
    stddev = variance ** 0.5
    latest = values[-1]
    if stddev > 0 and abs(latest - avg) > 3 * stddev:
        return "latest datapoint deviates more than 3 standard deviations from mean"
    return None


def summarize_metric(metric: str, start_time: Optional[str] = None, end_time: Optional[str] = None) -> MetricSummary:
    api_key = os.environ.get("DATADOG_API_KEY")
    app_key = os.environ.get("DATADOG_APP_KEY")
    if not api_key or not app_key:
        raise EnvironmentError("DATADOG_API_KEY and DATADOG_APP_KEY are required")

    end_dt = _parse_time(end_time)
    start_dt = _parse_time(start_time) if start_time else end_dt - timedelta(hours=1)

    url = "https://api.datadoghq.com/api/v1/query"
    params = {
        "from": int(start_dt.timestamp()),
        "to": int(end_dt.timestamp()),
        "query": metric,
    }
    headers = {
        "DD-API-KEY": api_key,
        "DD-APPLICATION-KEY": app_key,
        "Accept": "application/json",
    }
    response = requests.get(url, headers=headers, params=params, timeout=30)
    response.raise_for_status()
    payload: Dict[str, Any] = response.json()

    values: List[float] = []
    for series in payload.get("series", []):
        for point in series.get("pointlist", []):
            if point and len(point) >= 2 and point[1] is not None:
                values.append(float(point[1]))

    minimum = min(values) if values else None
    maximum = max(values) if values else None
    average = (sum(values) / len(values)) if values else None
    latest = values[-1] if values else None
    trend = _infer_trend(values)
    anomaly_reason = _detect_anomaly(values)

    return MetricSummary(
        metric=metric,
        start_time=start_dt.isoformat(),
        end_time=end_dt.isoformat(),
        sample_count=len(values),
        minimum=minimum,
        maximum=maximum,
        average=average,
        latest=latest,
        trend=trend,
        anomaly_detected=anomaly_reason is not None,
        anomaly_reason=anomaly_reason,
    )
