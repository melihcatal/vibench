from datetime import datetime
from typing import Any, Dict

from observability_client import get_client
from observability_models import MetricWindowRequest, metric_query_payload


def query_metric_window(
    metric_name: str,
    start_time: Any,
    end_time: Any,
    dimensions: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    request = MetricWindowRequest(
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        dimensions=dimensions,
    )
    client = get_client()
    payload = metric_query_payload(
        request.metric_name, request.start_time, request.end_time, request.dimensions
    )
    query = (
        f"avg:{request.metric_name}{{{','.join(f'{k}:{v}' for k, v in payload['dimensions'].items())}}}"
        if payload["dimensions"]
        else f"avg:{request.metric_name}"
    )
    start = int(datetime.fromisoformat(payload["start_time"]).timestamp())
    end = int(datetime.fromisoformat(payload["end_time"]).timestamp())
    return client.query_metrics(query, start, end)
