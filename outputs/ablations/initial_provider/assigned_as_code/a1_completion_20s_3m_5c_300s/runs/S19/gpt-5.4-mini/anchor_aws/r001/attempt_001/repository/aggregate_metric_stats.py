from datetime import datetime, timezone

from observability_client import load_config, cloudwatch_client
from observability_models import build_dimensions


def aggregate_metric_stats(payload, config=None):
    cfg = load_config(config)
    client = cloudwatch_client(config)
    response = client.get_metric_statistics(
        Namespace=cfg.namespace,
        MetricName=payload["metric"],
        Dimensions=build_dimensions(cfg.dimensions),
        StartTime=datetime.fromtimestamp(payload["start_time"], timezone.utc),
        EndTime=datetime.fromtimestamp(payload["end_time"], timezone.utc),
        Period=cfg.period_seconds,
        Statistics=["Average", "Sum", "Minimum", "Maximum", "SampleCount"],
    )
    datapoints = response.get("Datapoints", [])
    values = [float(p.get("Average", p.get("Sum", 0.0))) for p in datapoints if p]
    return {
        "metric": payload["metric"],
        "summary": {
            "count": len(values),
            "average": sum(values) / len(values) if values else None,
            "minimum": min(values) if values else None,
            "maximum": max(values) if values else None,
        },
        "points": sorted(
            [{"timestamp": p["Timestamp"].timestamp(), "value": float(p.get("Average", p.get("Sum", 0.0)))} for p in datapoints],
            key=lambda item: item["timestamp"],
        ),
    }
