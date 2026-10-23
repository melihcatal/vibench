from datetime import datetime, timezone

from observability_client import load_config, cloudwatch_client
from observability_models import build_dimensions, normalize_points, summarize_series


def compare_metric_series(payload, config=None):
    cfg = load_config(config)
    client = cloudwatch_client(config)

    def fetch(dimensions):
        response = client.get_metric_statistics(
            Namespace=cfg.namespace,
            MetricName=payload["metric"],
            Dimensions=build_dimensions(dimensions),
            StartTime=datetime.fromtimestamp(payload["start_time"], timezone.utc),
            EndTime=datetime.fromtimestamp(payload["end_time"], timezone.utc),
            Period=cfg.period_seconds,
            Statistics=["Average"],
        )
        return normalize_points([{"timestamp": p["Timestamp"].timestamp(), "value": float(p["Average"])} for p in response.get("Datapoints", [])])

    left = fetch(payload.get("left_dimensions", {}))
    right = fetch(payload.get("right_dimensions", {}))
    left_summary = summarize_series(left)
    right_summary = summarize_series(right)
    return {
        "metric": payload["metric"],
        "left": {"points": left, "summary": left_summary},
        "right": {"points": right, "summary": right_summary},
        "difference": {
            "average": (left_summary["average"] or 0.0) - (right_summary["average"] or 0.0),
            "change": (left_summary["change"] or 0.0) - (right_summary["change"] or 0.0),
        },
    }
