from datetime import timedelta

from observability_client import cloudwatch_client, load_config
from observability_models import (
    MetricWindowRequest,
    normalize_datapoints,
    normalize_dimensions,
    utc_now,
)


def filter_metric_dimensions(
    metric_name=None, namespace=None, minutes=60, period=300, dimensions=None
):
    cfg = load_config()
    req = MetricWindowRequest(
        metric_name=metric_name or cfg.metric_name,
        namespace=namespace or cfg.namespace,
        start_time=utc_now() - timedelta(minutes=minutes),
        end_time=utc_now(),
        period=period,
        dimensions=dimensions,
    )
    resp = cloudwatch_client().get_metric_statistics(
        Namespace=req.namespace,
        MetricName=req.metric_name,
        StartTime=req.start_time,
        EndTime=req.end_time,
        Period=req.period,
        Statistics=list(req.statistics),
        Dimensions=normalize_dimensions(req.dimensions),
    )
    datapoints = normalize_datapoints(resp.get("Datapoints", []))
    return [
        point
        for point in datapoints
        if all(point.get(k) is not None for k in ("Timestamp",))
    ]
