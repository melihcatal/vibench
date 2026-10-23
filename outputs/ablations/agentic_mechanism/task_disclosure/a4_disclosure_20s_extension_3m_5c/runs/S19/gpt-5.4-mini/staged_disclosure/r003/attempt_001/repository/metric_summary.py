import json
import os
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional

from datadog_api_client import ApiClient
from datadog_api_client.v1.api.metrics_api import MetricsApi
from datadog_api_client.v1.model.query_timeseries_points import QueryTimeseriesPoints
from datadog_api_client.v1.model.query_timeseries_response import QueryTimeseriesResponse
from datadog_api_client.v1.model.query_value import QueryValue
from datadog_api_client.v1.model.query_formula import QueryFormula
from datadog_api_client.v1.model.query import Query
from datadog_api_client.v1.model.query_sort import QuerySort
from datadog_api_client.v1.model.query_results import QueryResults
from datadog_api_client.v1.model.metric_payload import MetricPayload
from datadog_api_client.v1.model.metric_data import MetricData
from datadog_api_client.v1.model.metric_point import MetricPoint
from datadog_api_client.v1.configuration import Configuration


def _build_client() -> ApiClient:
    config = Configuration()
    if os.getenv("DD_SITE"):
        config.server_variables["site"] = os.getenv("DD_SITE")
    config.api_key["apiKeyAuth"] = os.getenv("DD_API_KEY", "")
    config.api_key["appKeyAuth"] = os.getenv("DD_APP_KEY", "")
    return ApiClient(config)


def _fetch_series(metric_name: str, hours: int = 24) -> List[float]:
    end = datetime.now(timezone.utc)
    start = end - timedelta(hours=hours)
    with _build_client() as api_client:
        api = MetricsApi(api_client)
        resp = api.query_metrics(
            _from=int(start.timestamp()),
            to=int(end.timestamp()),
            query=f"avg:{metric_name}{{*}}.rollup(avg, 300)",
        )
    values: List[float] = []
    series = getattr(resp, "series", []) or []
    for item in series:
        points = getattr(item, "pointlist", []) or []
        for point in points:
            if point and len(point) >= 2 and point[1] is not None:
                values.append(float(point[1]))
    return values


def _summarize(values: List[float]) -> Dict[str, Any]:
    if not values:
        return {"status": "no_data", "summary": "No metric data returned."}
    recent = values[-6:]
    earlier = values[:-6] if len(values) > 6 else values
    recent_avg = sum(recent) / len(recent)
    earlier_avg = sum(earlier) / len(earlier)
    delta = recent_avg - earlier_avg
    pct = (delta / earlier_avg * 100.0) if earlier_avg else None
    peak = max(values)
    trough = min(values)
    anomaly = abs(recent_avg - earlier_avg) > (0.25 * abs(earlier_avg) if earlier_avg else 1.0)
    trend = "upward" if delta > 0 else "downward" if delta < 0 else "flat"
    summary = {
        "status": "ok",
        "trend": trend,
        "recent_avg": round(recent_avg, 4),
        "baseline_avg": round(earlier_avg, 4),
        "delta": round(delta, 4),
        "pct_change": round(pct, 2) if pct is not None else None,
        "peak": round(peak, 4),
        "trough": round(trough, 4),
        "anomaly_suspected": anomaly,
    }
    return summary


def summarize_metric(metric_name: Optional[str] = None) -> Dict[str, Any]:
    metric = metric_name or os.getenv("DD_METRIC_NAME", "system.cpu.user")
    values = _fetch_series(metric)
    result = _summarize(values)
    result["metric"] = metric
    result["provider"] = "Datadog"
    return result


def main() -> None:
    print(json.dumps(summarize_metric(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
