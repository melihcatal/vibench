from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, Optional

from observability_client import build_metric_request, get_metric_statistics
from observability_models import aggregate_points


def aggregate_metric_stats(
    metric_name: str,
    start_time: datetime,
    end_time: datetime,
    namespace: str = "AWS/EC2",
    period: int = 300,
    dimensions: Optional[Dict[str, str]] = None,
    unit: Optional[str] = None,
) -> Dict[str, Any]:
    request = build_metric_request(
        metric_name=metric_name,
        start_time=start_time,
        end_time=end_time,
        namespace=namespace,
        period=period,
        stat="Average",
        dimensions=dimensions,
        unit=unit,
    )
    response = get_metric_statistics(request)
    aggregate = aggregate_points(
        metric_name=metric_name,
        namespace=namespace,
        datapoints=response.get("Datapoints", []),
        start_time=start_time,
        end_time=end_time,
    )
    return {
        "provider": "amazon-cloudwatch",
        "metric": aggregate.metric_name,
        "namespace": aggregate.namespace,
        "sample_count": aggregate.sample_count,
        "minimum": aggregate.minimum,
        "maximum": aggregate.maximum,
        "average": aggregate.average,
        "sum": aggregate.sum,
        "unit": aggregate.unit,
        "start_time": aggregate.start_time,
        "end_time": aggregate.end_time,
    }
