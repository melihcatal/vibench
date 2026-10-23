from __future__ import annotations

from typing import List

from observability_client import cloudwatch_client
from observability_models import MetricWindowRequest, normalize_cloudwatch_datapoints


CLOUDWATCH_PROVIDER = "monitoring.amazonaws.com"


def query_metric_window(request: MetricWindowRequest) -> List[dict]:
    client = cloudwatch_client()
    response = client.get_metric_statistics(
        Namespace=request.namespace,
        MetricName=request.metric_name,
        Dimensions=[{"Name": k, "Value": v} for k, v in request.dimensions.items()],
        StartTime=request.start_time,
        EndTime=request.end_time,
        Period=request.period,
        Statistics=[request.stat],
    )
    return [
        {
            "timestamp": point.timestamp,
            "value": point.value,
            "unit": point.unit,
            "provider": CLOUDWATCH_PROVIDER,
        }
        for point in normalize_cloudwatch_datapoints(response.get("Datapoints", []), request.stat)
    ]
