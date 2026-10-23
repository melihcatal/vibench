from datetime import timedelta

from observability_client import cloudwatch_client, load_config
from observability_models import normalize_datapoints, utc_now


def metric_summary(metric_name=None, namespace=None, minutes=120, period=300):
    cfg = load_config()
    resp = cloudwatch_client().get_metric_statistics(
        Namespace=namespace or cfg.namespace,
        MetricName=metric_name or cfg.metric_name,
        StartTime=utc_now() - timedelta(minutes=minutes),
        EndTime=utc_now(),
        Period=period,
        Statistics=["Average", "Sum"],
        Dimensions=[],
    )
    points = normalize_datapoints(resp.get("Datapoints", []))
    values = [p.get("Average") for p in points if p.get("Average") is not None]
    return {
        "count": len(values),
        "latest": values[-1] if values else None,
        "minimum": min(values) if values else None,
        "maximum": max(values) if values else None,
    }
