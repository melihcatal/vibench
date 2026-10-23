from __future__ import annotations

import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

import requests


@dataclass(frozen=True)
class MetricDatapoint:
    timestamp: datetime
    value: float


def _parse_iso8601(value: str) -> datetime:
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    dt = datetime.fromisoformat(value)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt


def query_metric_window(
    metric_name: str,
    window_minutes: int = 60,
    *,
    project_id: Optional[str] = None,
    alignment_period_seconds: int = 60,
) -> List[MetricDatapoint]:
    api_key = os.environ.get("MIXPANEL_SERVICE_ACCOUNT_SECRET")
    if not api_key:
        raise RuntimeError("Missing MIXPANEL_SERVICE_ACCOUNT_SECRET")

    project_id = project_id or os.environ.get("MIXPANEL_PROJECT_ID")
    if not project_id:
        raise RuntimeError("Missing MIXPANEL_PROJECT_ID")

    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=window_minutes)

    url = "https://eu.mixpanel.com/api/query/engage"
    params: Dict[str, Any] = {
        "project_id": project_id,
        "event": metric_name,
        "from_date": start_time.date().isoformat(),
        "to_date": end_time.date().isoformat(),
        "unit": "minute",
        "interval": alignment_period_seconds,
    }
    response = requests.get(url, params=params, auth=(api_key, ""), timeout=30)
    response.raise_for_status()
    payload = response.json()

    points: List[MetricDatapoint] = []
    data = payload.get("data", []) if isinstance(payload, dict) else []
    for item in data:
        if not isinstance(item, dict):
            continue
        ts = item.get("timestamp") or item.get("time") or item.get("date")
        val = item.get("value") or item.get("count") or item.get("total")
        if ts is None or val is None:
            continue
        points.append(MetricDatapoint(timestamp=_parse_iso8601(str(ts)), value=float(val)))

    points.sort(key=lambda p: p.timestamp)
    return [p for p in points if start_time <= p.timestamp <= end_time]
