from datetime import datetime, timezone


def normalize_metric_window(payload):
    return {
        "metric": payload["metric"],
        "start_time": float(payload["start_time"]),
        "end_time": float(payload["end_time"]),
    }


def normalize_dimensions(dimensions):
    return [{"Name": k, "Value": v} for k, v in sorted((dimensions or {}).items())]


def datapoints_to_series(datapoints, value_key="Average"):
    points = []
    for point in datapoints:
        value = point.get(value_key)
        if value is None:
            continue
        points.append({"timestamp": point["Timestamp"].timestamp(), "value": float(value)})
    return sorted(points, key=lambda p: p["timestamp"])


def timestamp_range(payload):
    return datetime.fromtimestamp(payload["start_time"], timezone.utc), datetime.fromtimestamp(payload["end_time"], timezone.utc)
