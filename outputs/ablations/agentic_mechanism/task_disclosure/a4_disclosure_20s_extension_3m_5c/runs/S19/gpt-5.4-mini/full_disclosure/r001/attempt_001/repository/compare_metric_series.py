import os
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import requests


OPENAI_METRICS_API_BASE = os.getenv("OPENAI_METRICS_API_BASE", "https://api.openai.com")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_METRICS_MODEL = os.getenv("OPENAI_METRICS_MODEL", "openai/gpt-5.4-mini")


def _headers() -> Dict[str, str]:
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "X-Model-Id": OPENAI_METRICS_MODEL,
    }
    return headers


def _normalize_series(items: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    normalized = []
    for item in items:
        timestamp = item.get("timestamp") or item.get("time")
        value = item.get("value")
        if isinstance(timestamp, (int, float)):
            timestamp = datetime.fromtimestamp(timestamp, tz=timezone.utc).isoformat()
        normalized.append({"timestamp": timestamp, "value": value})
    return normalized


def compare_metric_series(
    metric_name: str,
    start_time: str,
    end_time: str,
    left_filter: Optional[Dict[str, str]] = None,
    right_filter: Optional[Dict[str, str]] = None,
) -> Dict[str, Any]:
    url = f"{OPENAI_METRICS_API_BASE.rstrip('/')}/v1/metrics/{metric_name}/compare"
    payload = {
        "start_time": start_time,
        "end_time": end_time,
        "left_filter": left_filter or {},
        "right_filter": right_filter or {},
    }
    response = requests.post(url, headers=_headers(), json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    left_series = _normalize_series(data.get("left_series", []))
    right_series = _normalize_series(data.get("right_series", []))
    return {
        "metric_name": metric_name,
        "window": {"start_time": start_time, "end_time": end_time},
        "left_filter": left_filter or {},
        "right_filter": right_filter or {},
        "left_series": left_series,
        "right_series": right_series,
        "summary": data.get("summary", {}),
    }
