from datetime import datetime
from typing import Any, Dict, Optional

from observability_client import (
    build_dimensions,
    cloudwatch_client,
    resolve_metric_name,
)
from observability_models import normalize_datapoints, summarize_points


def aggregate_metric_stats(
    start_time: datetime,
    end_time: datetime,
    metric_name: Optional[str] = None,
    namespace: str = "AWS/EC2",
    dimensions: Optional[Dict[str, str]] = None,
    period: int = 300,
) -> dict[str, Any]:
    metric = resolve_metric_name(metric_name)
    response = cloudwatch_client().get_metric_statistics(
        Namespace=namespace,
        MetricName=metric,
        StartTime=start_time,
        EndTime=end_time,
        Period=period,
        Statistics=["Average", "Sum", "Minimum", "Maximum", "SampleCount"],
        Dimensions=build_dimensions(dimensions),
    )
    datapoints = normalize_datapoints(response.get("Datapoints", []))
    return {
        "metric_name": metric,
        "namespace": namespace,
        "summary": summarize_points(datapoints),
        "datapoints": datapoints,
    }
