from datetime import datetime, timezone

import boto3

from observability_models import normalize_dimensions


def aggregate_metric_stats(payload, config=None):
    config = config or {}
    client = boto3.client("cloudwatch", region_name=config.get("region"))
    response = client.get_metric_statistics(
        Namespace=config["namespace"],
        MetricName=payload["metric"],
        Dimensions=normalize_dimensions(config.get("dimensions")),
        StartTime=datetime.fromtimestamp(payload["start_time"], timezone.utc),
        EndTime=datetime.fromtimestamp(payload["end_time"], timezone.utc),
        Period=config.get("period_seconds", 60),
        Statistics=["Average", "Sum", "Minimum", "Maximum", "SampleCount"],
    )
    datapoints = response.get("Datapoints", [])
    if not datapoints:
        return {"statistics": {"average": None, "sum": None, "minimum": None, "maximum": None, "sample_count": 0}}
    averages = [float(point["Average"]) for point in datapoints if "Average" in point]
    sums = [float(point["Sum"]) for point in datapoints if "Sum" in point]
    mins = [float(point["Minimum"]) for point in datapoints if "Minimum" in point]
    maxs = [float(point["Maximum"]) for point in datapoints if "Maximum" in point]
    sample_count = sum(int(point.get("SampleCount", 0)) for point in datapoints)
    return {
        "statistics": {
            "average": sum(averages) / len(averages) if averages else None,
            "sum": sum(sums) if sums else None,
            "minimum": min(mins) if mins else None,
            "maximum": max(maxs) if maxs else None,
            "sample_count": sample_count,
        }
    }
