from datetime import datetime, timezone

from observability_client import cloudwatch_client, load_observability_config
from observability_models import normalize_dimensions, normalize_points


def aggregate_metric_stats(payload, config=None):
    config = load_observability_config(config)
    client = cloudwatch_client(config)
    response = client.get_metric_statistics(
        Namespace=config["namespace"],
        MetricName=payload["metric"],
        Dimensions=[{"Name": k, "Value": v} for k, v in normalize_dimensions(config.get("dimensions")).items()],
        StartTime=datetime.fromtimestamp(payload["start_time"], timezone.utc),
        EndTime=datetime.fromtimestamp(payload["end_time"], timezone.utc),
        Period=config.get("period_seconds", 60),
        Statistics=payload.get("statistics", ["Average", "Minimum", "Maximum", "SampleCount"]),
    )
    return {"points": normalize_points([{ "timestamp": p["Timestamp"].timestamp(), "value": float(p.get(payload.get("preferred_stat", "Average"), p.get("Average", 0.0))) } for p in response["Datapoints"]])}
