from datetime import datetime
from typing import Any, Dict, Optional

from observability_client import (
    build_dimensions,
    cloudwatch_client,
    resolve_metric_name,
)
from observability_models import MetricWindowRequest, normalize_datapoints


def query_metric_window(
    start_time: datetime,
    end_time: datetime,
    metric_name: Optional[str] = None,
    namespace: str = "AWS/EC2",
    dimensions: Optional[Dict[str, str]] = None,
    period: int = 300,
    statistics: Optional[list[str]] = None,
) -> dict[str, Any]:
    metric = resolve_metric_name(metric_name)
    request = MetricWindowRequest(
        metric,
        start_time,
        end_time,
        namespace,
        dimensions,
        period,
        statistics or ["Average"],
    )
    response = cloudwatch_client().get_metric_statistics(
        Namespace=request.namespace,
        MetricName=request.metric_name,
        StartTime=request.start_time,
        EndTime=request.end_time,
        Period=request.period,
        Statistics=request.statistics,
        Dimensions=build_dimensions(request.dimensions),
    )
    datapoints = normalize_datapoints(response.get("Datapoints", []))
    return {"metric_name": metric, "namespace": namespace, "datapoints": datapoints}
