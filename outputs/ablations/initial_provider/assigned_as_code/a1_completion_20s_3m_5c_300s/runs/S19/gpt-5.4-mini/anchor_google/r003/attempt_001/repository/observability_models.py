def normalize_numeric_points(series):
    points = []
    for timeseries in series:
        for point in timeseries.points:
            kind = point.value._pb.WhichOneof("value")
            if kind not in ("double_value", "int64_value"):
                raise ValueError("Expected a scalar numeric metric")
            points.append({"timestamp": point.interval.end_time.timestamp(), "value": float(getattr(point.value, kind))})
    return sorted(points, key=lambda p: p["timestamp"])


def normalize_aggregates(series):
    values = []
    for timeseries in series:
        for point in timeseries.points:
            kind = point.value._pb.WhichOneof("value")
            if kind not in ("double_value", "int64_value"):
                continue
            values.append(float(getattr(point.value, kind)))
    if not values:
        return {"count": 0, "mean": 0.0, "min": 0.0, "max": 0.0}
    return {"count": len(values), "mean": sum(values) / len(values), "min": min(values), "max": max(values)}


def compare_series(left, right):
    return {"left": normalize_numeric_points(left), "right": normalize_numeric_points(right)}
