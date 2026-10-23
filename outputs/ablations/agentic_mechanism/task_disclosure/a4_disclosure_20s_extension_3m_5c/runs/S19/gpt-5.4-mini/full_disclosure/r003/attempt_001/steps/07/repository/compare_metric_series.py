import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

import requests


@dataclass
class MetricSeriesComparison:
    left: List[Dict[str, Any]]
    right: List[Dict[str, Any]]
    metric: str
    start: str
    end: str
    left_filter: Dict[str, Any]
    right_filter: Dict[str, Any]


def _parse_time(value: Optional[str], default: datetime) -> datetime:
    if not value:
        return default
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _normalize_filters(filters: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    return filters or {}


def compare_metric_series(
    metric: str,
    left_filter: Optional[Dict[str, Any]] = None,
    right_filter: Optional[Dict[str, Any]] = None,
    start: Optional[str] = None,
    end: Optional[str] = None,
    granularity: str = "PT1H",
) -> MetricSeriesComparison:
    api_key = os.environ["DATADOG_API_KEY"]
    app_key = os.environ["DATADOG_APP_KEY"]
    base_url = os.getenv("DATADOG_API_BASE_URL", "https://api.datadoghq.com")

    end_dt = _parse_time(end, datetime.now(timezone.utc))
    start_dt = _parse_time(start, end_dt - timedelta(hours=1))

    payload = {
        "data": {
            "type": "timeseries_request",
            "attributes": {
                "from": start_dt.isoformat().replace("+00:00", "Z"),
                "to": end_dt.isoformat().replace("+00:00", "Z"),
                "queries": [
                    {
                        "data_source": "metrics",
                        "query": metric,
                        "aggregator": "avg",
                        "interval": granularity,
                        "group_by": [],
                        "filter": _normalize_filters(left_filter),
                    },
                    {
                        "data_source": "metrics",
                        "query": metric,
                        "aggregator": "avg",
                        "interval": granularity,
                        "group_by": [],
                        "filter": _normalize_filters(right_filter),
                    },
                ],
            },
        }
    }

    headers = {
        "DD-API-KEY": api_key,
        "DD-APPLICATION-KEY": app_key,
        "Content-Type": "application/json",
    }

    response = requests.post(
        f"{base_url}/api/v2/query/timeseries",
        json=payload,
        headers=headers,
        timeout=30,
    )
    response.raise_for_status()
    data = response.json()
    series = data.get("data", {}).get("attributes", {}).get("series", [])
    left = series[0] if len(series) > 0 else {}
    right = series[1] if len(series) > 1 else {}

    return MetricSeriesComparison(
        left=[left] if left else [],
        right=[right] if right else [],
        metric=metric,
        start=payload["data"]["attributes"]["from"],
        end=payload["data"]["attributes"]["to"],
        left_filter=_normalize_filters(left_filter),
        right_filter=_normalize_filters(right_filter),
    )


__all__ = ["MetricSeriesComparison", "compare_metric_series"]
