from datetime import datetime, timedelta, timezone
from typing import Optional

from observability_client import cloudwatch_client, load_config
from observability_models import MetricWindowRequest, MetricWindowResponse, normalize_dimensions


def query_metric_window(
    metric_name: Optional[str] = None,
    namespace: Optional[str] = None,
    dimensions: Optional[dict] = None,
    minutes: int = 60,
    period: int = 300,
) -> MetricWindowResponse:
    cfg = load_config(namespace=namespace, metric_name=metric_name)
    end_time = datetime.now(timezone.utc)
    start_time = end_time - timedelta(minutes=minutes)
    request = MetricWindowRequest(
        namespace=cfg.namespace,
        metric_name=cfg.metric_name,
        start_time=start_time,
        end_time=end_time,
        period=period,
        dimensions=dimensions,
    )
    client = cloudwatch_client()
    response = client.get_metric_statistics(
        Namespace=request.namespace,
        MetricName=request.metric_name,
        Dimensions=normalize_dimensions(request.dimensions),
        StartTime=request.start_time,
        EndTime=request.end_time,
        Period=request.period,
        Statistics=request.statistics,
    )
    datapoints = sorted(response.get("Datapoints", []), key=lambda x: x["Timestamp"])
    timestamps = [point["Timestamp"] for point in datapoints]
    values = [float(point.get("Average", point.get("Sum", 0.0))) for point in datapoints]
    return MetricWindowResponse(timestamps=timestamps, values=values, metadata={"request": request, "raw": response})
