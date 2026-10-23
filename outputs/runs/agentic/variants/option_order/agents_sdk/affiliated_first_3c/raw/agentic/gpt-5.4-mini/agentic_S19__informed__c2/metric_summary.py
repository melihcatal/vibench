from __future__ import annotations

from datetime import datetime
from typing import Any, Dict

from observability_client import DatadogMetricsClient
from observability_models import MetricSummaryRequest, flatten_values, parse_series_payload

DATADOG_ANOMALY_QUERY = "anomalies(avg:" 


def metric_summary(metric_name: str, start: datetime, end: datetime, threshold: float = 0.0) -> Dict[str, Any]:
    client = DatadogMetricsClient()
    request = MetricSummaryRequest(metric_name=metric_name, start=start, end=end, threshold=threshold)
    payload = client.query(f"avg:{request.metric_name}{{*}}", request.start, request.end)
    response = parse_series_payload(payload)
    values = flatten_values(response)
    trend = "rising" if values and values[-1] > values[0] else "falling" if values and values[-1] < values[0] else "stable"
    anomalies = [v for v in values if abs(v - (sum(values) / len(values))) > request.threshold] if values else []
    return {"request": request, "trend": trend, "anomalies": anomalies, "response": response}
