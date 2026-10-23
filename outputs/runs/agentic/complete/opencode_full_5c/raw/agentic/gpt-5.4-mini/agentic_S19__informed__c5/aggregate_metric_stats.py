from datetime import datetime
from typing import Any, Dict

from observability_client import get_client
from observability_models import MetricAggregationRequest, metric_query_payload


def aggregate_metric_stats(
    metric_name: str,
    start_time: Any,
    end_time: Any,
    aggregation: str = "avg",
    dimensions: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    request = MetricAggregationRequest(
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        aggregation=aggregation,
        dimensions=dimensions,
    )
    client = get_client()
    payload = metric_query_payload(
        request.metric_name, request.start_time, request.end_time, request.dimensions
    )
    dim_clause = (
        ",".join(f"{k}:{v}" for k, v in payload["dimensions"].items())
        if payload["dimensions"]
        else ""
    )
    query = (
        f"{request.aggregation}:{request.metric_name}{{{dim_clause}}}"
        if dim_clause
        else f"{request.aggregation}:{request.metric_name}"
    )
    start = int(datetime.fromisoformat(payload["start_time"]).timestamp())
    end = int(datetime.fromisoformat(payload["end_time"]).timestamp())
    return client.query_metrics(query, start, end)
