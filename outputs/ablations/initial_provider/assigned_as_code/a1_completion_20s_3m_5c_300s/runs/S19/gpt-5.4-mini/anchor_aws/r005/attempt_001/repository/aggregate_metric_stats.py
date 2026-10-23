from observability_client import cloudwatch_client
from observability_models import build_dimensions, normalize_datapoints, to_utc_datetime


def aggregate_metric_stats(payload, config=None):
    config = config or {}
    client = cloudwatch_client(config)
    response = client.get_metric_statistics(
        Namespace=config["namespace"],
        MetricName=payload["metric"],
        Dimensions=build_dimensions(config.get("dimensions")),
        StartTime=to_utc_datetime(payload["start_time"]),
        EndTime=to_utc_datetime(payload["end_time"]),
        Period=config.get("period_seconds", 60),
        Statistics=["Average", "Sum", "Minimum", "Maximum", "SampleCount"],
    )
    datapoints = response.get("Datapoints", [])
    points = normalize_datapoints(datapoints, "Average")
    stats = {
        "average": sum(p["value"] for p in points) / len(points) if points else 0.0,
        "minimum": min((p["value"] for p in points), default=0.0),
        "maximum": max((p["value"] for p in points), default=0.0),
        "count": len(points),
    }
    return {"points": points, "statistics": stats}
