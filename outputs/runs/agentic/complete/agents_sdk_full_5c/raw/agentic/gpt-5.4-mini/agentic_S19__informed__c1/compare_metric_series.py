from __future__ import annotations

from datetime import timedelta

from observability_client import DatadogMetricsClient, utc_now
from observability_models import MetricComparisonResponse, MetricWindowRequest, serialize_datapoints


def compare_metric_series(metric_name: str, left_dimensions: dict[str, str], right_dimensions: dict[str, str], minutes: int = 60) -> MetricComparisonResponse:
    end_time = utc_now()
    client = DatadogMetricsClient()
    left_req = MetricWindowRequest(metric_name=metric_name, start_time=end_time - timedelta(minutes=minutes), end_time=end_time, dimensions=left_dimensions)
    right_req = MetricWindowRequest(metric_name=metric_name, start_time=end_time - timedelta(minutes=minutes), end_time=end_time, dimensions=right_dimensions)
    left_payload = client.query_series(left_req)
    right_payload = client.query_series(right_req)
    left_points = serialize_datapoints({"timestamp": p[0] / 1000.0 if isinstance(p, list) and p else None, "value": p[1], "dimensions": left_dimensions} for p in left_payload.get("series", [{}])[0].get("pointlist", []) if p)
    right_points = serialize_datapoints({"timestamp": p[0] / 1000.0 if isinstance(p, list) and p else None, "value": p[1], "dimensions": right_dimensions} for p in right_payload.get("series", [{}])[0].get("pointlist", []) if p)
    return MetricComparisonResponse(metric_name=metric_name, left_label=str(left_dimensions), right_label=str(right_dimensions), left_series=left_points, right_series=right_points, raw={"left": left_payload, "right": right_payload})
