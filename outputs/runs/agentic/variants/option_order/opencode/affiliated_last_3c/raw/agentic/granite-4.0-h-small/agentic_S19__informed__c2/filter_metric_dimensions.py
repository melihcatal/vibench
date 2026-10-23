# [SAME-SCENARIO] filter_metric_dimensions.py

# Query metric data filtered by resource labels or dimensions.
# Provider: Amazon CloudWatch Metrics (boto3 SDK)

import os
from typing import List, Dict, Any

from .observability_client import get_cloudwatch_client
from .observability_models import CloudWatchMetricStatQuery, normalize_metric_response


def filter_metric_dimensions(
    metric_name: str,
    dimensions: List[Dict[str, Any]],
    namespace: str = "AWS/EC2",
    period: int = 60,
    statistics: List[str] = ["Average"],
) -> List[Dict[str, Any]]:
    """
    Retrieves metric data filtered by the supplied *dimensions* dictionary list.
    Dimensions can be any key/value pairs (e.g., [{\"InstanceId\": \"i-12345\"}]).

    Returns aggregated stats (Average by default) for the filtered series.
    """
    client = get_cloudwatch_client()
    query = CloudWatchMetricStatQuery(
        namespace=namespace,
        metric_name=metric_name,
        start_time=(datetime.utcnow() - timedelta(minutes=60)).isoformat() + "Z",
        end_time=datetime.utcnow().isoformat() + "Z",
        period=period,
        statistics=statistics,
        dimensions=dimensions,
    )
    api_params = {
        "Namespace": query.namespace,
        "MetricName": query.metric_name,
        "StartTime": query.start_time,
        "EndTime": query.end_time,
        "Period": query.period,
        "Statistics": query.statistics,
        "Dimensions": query.dimensions,
    }
    try:
        raw_resp = client.get_metric_statistics(**api_params)
    except Exception as exc:
        raise RuntimeError(f"Filtered stats query failed for {metric_name}") from exc
    return normalize_metric_response(raw_resp)
