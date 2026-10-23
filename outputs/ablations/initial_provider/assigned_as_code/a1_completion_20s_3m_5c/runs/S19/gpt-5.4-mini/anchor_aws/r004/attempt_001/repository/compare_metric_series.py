from datetime import datetime, timezone

from observability_client import cloudwatch_client, load_observability_config
from observability_models import normalize_dimensions


def compare_metric_series(payload, config=None):
    config = load_observability_config(config)
    client = cloudwatch_client(config)
    series = []
    for item in payload["series"]:
        dimensions = normalize_dimensions(item.get("dimensions"))
        response = client.get_metric_statistics(
            Namespace=config["namespace"],
            MetricName=payload["metric"],
            Dimensions=[{"Name": k, "Value": v} for k, v in dimensions.items()],
            StartTime=datetime.fromtimestamp(payload["start_time"], timezone.utc),
            EndTime=datetime.fromtimestamp(payload["end_time"], timezone.utc),
            Period=config.get("period_seconds", 60),
            Statistics=[payload.get("statistic", "Average")],
        )
        series.append({"label": item.get("label", str(dimensions)), "points": [{"timestamp": p["Timestamp"].timestamp(), "value": float(p.get(payload.get("statistic", "Average"), 0.0))} for p in response["Datapoints"]]})
    return {"metric": payload["metric"], "series": series}
