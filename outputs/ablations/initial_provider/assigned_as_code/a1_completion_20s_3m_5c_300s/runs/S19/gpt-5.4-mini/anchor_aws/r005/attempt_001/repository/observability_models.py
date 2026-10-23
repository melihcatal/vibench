from datetime import datetime, timezone


def to_utc_datetime(value):
    if isinstance(value, datetime):
        return value.astimezone(timezone.utc)
    return datetime.fromtimestamp(float(value), timezone.utc)


def normalize_datapoints(datapoints, statistic="Average"):
    points = []
    for point in datapoints or []:
        value = point.get(statistic)
        if value is None and statistic != "Average":
            value = point.get("Average")
        if value is None:
            continue
        points.append({"timestamp": point["Timestamp"].timestamp(), "value": float(value)})
    return sorted(points, key=lambda p: p["timestamp"])


def build_dimensions(dimensions):
    return [{"Name": key, "Value": value} for key, value in (dimensions or {}).items()]
